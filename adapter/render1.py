import abc
import collections
import sys
import textwrap
from xml.sax.saxutils import escape


class Renderer(metaclass=abc.ABCMeta):

    """
    __subclasshook__ 재구현.
    isinstance()가 활용
    첫번째 인자로 전달된 객체가 두번쨰 인자로 전달된 클래스의 상위클래스인지 판단
    반환값: True/False => 추상기반클래스 쪽에서 코드 실행 멈춤 bool 값 반환
        : NotImplemented => 일반적인 상속 기능 동작
    """
    @classmethod
    def __subclasshook__(Class, Subclass):
        if Class is Renderer:  # 호출대상 클래스가 Renderer인지 검사
            attributes = collections.ChainMap(*(Superclass.__dict__
                    for Superclass in Subclass.__mro__))  # 각 클래스의 비공개 딕셔너리에 접근 후 딕셔너리로 이뤄진 튜플을 인자로 받아 단일 맵 뷰 반환, 튜플 생성
            methods = ("header", "paragraph", "footer")
            if all(method in attributes for method in methods):  # 모든 메서드가 attributes 맵에 있는지 검사 모든 메서드가 있으면 True 반환
                return True
        return NotImplemented  # Renderer의 하위 클래스가 요 함수 행위를 상속하지 않음: 인터페이스 세분화에 목적이 있기 떄문



MESSAGE = """This is a very short {} paragraph that demonstrates
the simple {} class."""

def main():
    paragraph1 = MESSAGE.format("plain-text", "TextRenderer")
    paragraph2 = """This is another short paragraph just so that we can
see two paragraphs in action."""
    title = "Plain Text"
    textPage = Page(title, TextRenderer(22))
    textPage.add_paragraph(paragraph1)
    textPage.add_paragraph(paragraph2)
    textPage.render()

    print()

    paragraph1 = MESSAGE.format("HTML", "HtmlRenderer")
    title = "HTML"
    file = sys.stdout
    htmlPage = Page(title, HtmlRenderer(HtmlWriter(file)))
    htmlPage.add_paragraph(paragraph1)
    htmlPage.add_paragraph(paragraph2)
    htmlPage.render()

    try:
        page = Page(title, HtmlWriter())
        page.render()
        print("ERROR! rendering with an invalid renderer")
    except TypeError as err:
        print(err)


# 인터페이스로 header(str), paragraph(str), footer()를 제공하는 한 실제 구현 클래스는 신경 안씀
class Page:

    def __init__(self, title, renderer):
        """
        전달된 객체가 Renderer 인스턴스임을 보장
        - assert isinstance(renderer, Renderer)를 사용하면
            1) TypeError 대신 AssertionError 발생
            2) 프로그램 실행 시 -O (optimize, 최적화) 옵션을 주면 assert 구문이 무시되기 때문에
               render() 에서 AttributeError 발생
        """
        if not isinstance(renderer, Renderer):
            raise TypeError("Expected object of type Renderer, got {}".
                    format(type(renderer).__name__))
        self.title = title
        self.renderer = renderer
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def render(self):
        self.renderer.header(self.title)
        for paragraph in self.paragraphs:
            self.renderer.paragraph(paragraph)
        self.renderer.footer()


# 인터페이스를 지원하는 클래스
class TextRenderer:

    def __init__(self, width=80, file=sys.stdout):
        self.width = width
        self.file = file
        self.previous = False

    def header(self, title):
        self.file.write("{0:^{2}}\n{1:^{2}}\n".format(title,
                "=" * len(title), self.width))

    def paragraph(self, text):
        if self.previous:
            self.file.write("\n")
        self.file.write(textwrap.fill(text, self.width))
        self.file.write("\n")
        self.previous = True

    # 인터페이스의 일부이므로 존재해야함
    def footer(self):
        pass


class HtmlWriter:
    """
     paragraph함수가 없어 Renderer 인터페이스의 요구사항을 충족시키지 않음 => Page 인스턴스에 직접 전달 못함
     해결
     - HtmlWriter를 상속한 클래스에 인터페이스 메서드 추가 -> 취약: 인터페이스 무결성 위반(인터페이스 메서드와 HtmlWriter 메서드가 섞여 있으므로)
     - 어댑터 만들기 (HtmlRenderer)
        :
    """

    def __init__(self, file=sys.stdout):
        self.file = file

    def header(self):
        self.file.write("<!doctype html>\n<html>\n")

    def title(self, title):
        self.file.write("<head><title>{}</title></head>\n".format(
                escape(title)))

    def start_body(self):
        self.file.write("<body>\n")

    def body(self, text):
        self.file.write("<p>{}</p>\n".format(escape(text)))

    def end_body(self):
        self.file.write("</body>\n")

    def footer(self):
        self.file.write("</html>\n")


# 기존 HtmlWirter 클래스에 새로운 인터페이스를 제공하는 래퍼에 불과
class HtmlRenderer:

    def __init__(self, htmlWriter):  # 객체 생성 시 HtmlWriter 얻고 , 실제 작업은 HtmlWriter 객체에 위임
        self.htmlWriter = htmlWriter

    # 인터페이스 메서드 제공
    def header(self, title):
        self.htmlWriter.header()
        self.htmlWriter.title(title)
        self.htmlWriter.start_body()

    def paragraph(self, text):
        self.htmlWriter.body(text)

    def footer(self):
        self.htmlWriter.end_body()
        self.htmlWriter.footer()


if __name__ == "__main__":
    main()
