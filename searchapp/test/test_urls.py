from django.test import TestCase
from django.test.utils import override_settings
from django.urls import resolve
from django.urls import path

from searchapp.views import ResultList

"""
UnitTestの書き方
・アプリケーションの下に test から始まるファイルを作る
・django.test.TestCaseを継承したクラスを作る
・メソッド名をtestから始める


メソッド                 確認事項
assertEqual(a, b)        a == b
assertNotEqual(a, b)     a != b
assertTrue(x)            bool(x) is True
assertFalse(x)           bool(x) is False

例外が発生したらOK
def test_exception2(self):
self.assertRaises(Exception, func)

"""

class UrlResolveTests(TestCase):
    """
    URL解決のテスト
    """

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_url_resolves_ResultList(self):
        """''(指定なし)で、クラスResultListを呼び出している事を検証 """
        found = resolve('result/')
        test = ResultList.__name__
        self.assertEqual(found.func.__name__, ResultList.__name__,'呼び出しているVIEWが想定と異なる')
