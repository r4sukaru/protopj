from django.test.utils import override_settings
# テストクラスに継承させるTestCaseをインポート
from django.test import TestCase
# reverse関数のインポート（URLの逆引きに必要）
from django.urls import reverse
# srhapp直下のmodelsをインポート
from searchapp import models
from searchapp.models import GoodsTBL
# ViewのResultListをインポート（factory_categoryとfactory_ticket関数が定義されている）
from searchapp.views import ResultList


# Create your tests here.

# Ticketというモデルのリスト作成に関するテストコードを定義するクラスを作成
class ResultListTest(TestCase):

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_post(self):
        # DBデータを事前に登録しておく
        GoodsTBL(category='02',search='カットソー').save()

        #チェック用
        check_title, check_category, check_price = '02', 'カットソー'

        # リクエストを擬似的に送ってくれるHTTPクライアント（self.cliant）でレスポンスオブジェクトを生成
        response = self.client.post(reverse('searchapp:iresult'), {'category':'02','search':'カットソー' })

        # 結果が正常に返ってきていることを確認
        assert response.status_code == 200

        #検索結果が1件であることを確認
        self.assertEqual(response.context['object_list'].count(),1)

        #検索結果の値突合
        self.assertEqual(response.context['object_list'].first().title, check_title)
        self.assertEqual(response.context['object_list'].first().category, check_category)
        self.assertEqual(response.context['object_list'].first().price, check_price)