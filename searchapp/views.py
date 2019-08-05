"""searchaappのソースコード"""
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Q
from .forms import CategorySearchForm
from .forms import GoodsSearchForm
from .models import GoodsTBL
from datetime import datetime


class Search(generic.ListView):
    """
    検索画面のクラス
    ※結合するタイミングで削除するクラス
    """

    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    template_name = 'searchapp/search.html'
    # クエリ結果を格納する変数の名前を定義している
    context_object_name = 'goods_search_result'

    # ①-1 post関数を定義(?)(taguchi)
    def post(self, request):
        """
        ユーザが入力した値を取得し、
        その値を元に商品の検索を実行
        検索結果をresult.htmlに返却する。
        """

        # ②-1(taguchi)
        # フォーム値をセッションに格納（他画面で使いたい）
        # 後からユーザが入力したフォームの値を格納するためのリストを作成（リスト名：form_value）
        form_value = [
            self.request.POST.get('category_name', None),
            self.request.POST.get('search_char', None)
        ]

        # ②-2(taguchi)　
        # ②-1で作成したフォームの値を格納するリストをセッション（request.session）に受け渡す
        request.session['form_value'] = form_value
        # generic/list.pyのget()メソッドが呼び出される　※本当にこのタイミング？もう少し上では？

        # ②-3(taguchi)
        # redirectでページを遷移する
        self.get(request)
        return redirect('searchapp:result')

    # ①-2(taguchi)
    # get_context_dataメソッドでcontextデータをテンプレートに渡すことが出来る
    def get_context_data(self, *, object_list=None, **kwargs):
        """
         フォームの初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # ①-3(taguchi)
        # 親クラスのメソッド呼び出し、変数contextに格納
        # context＝テンプレートに使用できる文字列タグの存在を定義　※辞書型しか格納できない
        context = super().get_context_data(**kwargs)

        # ①-4(taguchi)
        # category_name、search_charにそれぞれ空白の文字列を設定する
        category_name = ''
        search_char = ''

        # ①-5(taguchi)
        # 初期値を格納するための辞書型を作成、変数名は「default_data」
        # ①-4で設定した中身が空白文字列の変数を辞書の中に格納。
        default_data = {'category_name': category_name,
                        'search_char': search_char}

        # ①-6(taguchi)
        # 予めインポートしてあるフォームに初期値の空白を設定して、更にフォームを変数に格納する。
        # （文字列検索フォーム＝search_form）
        # （カテゴリ検索フォーム=category_form）
        search_form = GoodsSearchForm(initial=default_data)
        category_form = CategorySearchForm(initial=default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理

        # ①-7(taguchi)
        # ①-3で設定したcontextに①-6でフォームをつっこんだ変数を格納して
        # フォームの入っているリスト'search_value'をテンプレートに返す。
        context['search_value'] = [category_form, search_form]
        return context


class ResultList(generic.ListView):
    """検索結果一覧画面のクラス"""
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        """
        次画面に必要な情報（製品番号）をセッションに格納してリダイレクトする
        """
        # 1-5(result.htmlから)
        # sessionへ製品番号を保存
        request.session['g_de_productno'] = request.POST.get('productno', None)
        # 1-6
        # セッションからサイズと色を削除
        # 次画面でのブラウザバック使用時の為の設定
        if 'size' in request.session:
            del request.session['size']
        if 'color' in request.session:
            del request.session['color']
        # 1-7
        # redirect関数でdetailsクラスを呼び出す
        return redirect('searchapp:details')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
         条件に合った商品を一覧で表示するメソッド
        '''
        # 1-1
        # セッションの中にユーザの入力値が入っているかどうかの判定
        # ↑（検索押した後に動いているので基本的にはなにかしら入ってる：Nullではない）
        # 入っている場合は変数form_valueの中に前画面でユーザ入力値を格納したセッションを格納する

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
        else:
            form_value = ['', '']

        # 変数category_nameとsearch_charにユーザの入力値を格納する
        category_id = form_value[0]
        search_char = form_value[1]

        # 1-2
        # Qオブジェクトを作成。
        # exact=完全一致、contains=含む
        exact_cate = Q(categoryid__exact=category_id)
        contains_name = Q(goodsname__contains=search_char)
        contains_color = Q(colorname__contains=search_char)
        contains_price = Q(price__contains=search_char)
        contains_size = Q(sizename__contains=search_char)
        exact_ronsaku = Q(deleteflag__exact=0)
        lte_salesstartdate = Q(salesstartdate__lte=datetime.now().date())
        gt_salesenddate = Q(salesenddate__gt=datetime.now().date())
        exact_salesenddate = Q(salesenddate__exact=None)
        # 1-3
        # 入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
        # 分岐先で指定のクエリセットを発行し、変数goods_search_resultの中に格納する
        if form_value[0] == '':
            if form_value[1] == '':
                # カテゴリ×文字×
                # (全ての商品データ)
                goods_search_result = GoodsTBL.objects\
                .filter(exact_ronsaku& lte_salesstartdate\
                & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
            else:
                # カテゴリ×文字〇の時
                # (入力文字を値に含む商品データ)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_ronsaku\
                & (contains_name | contains_color | contains_price | contains_size)\
                & lte_salesstartdate& (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
        else:
            if form_value[1] == '':
                # カテゴリ〇文字×の時
                # (選択したカテゴリと同じカテゴリに設定した商品データ)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_cate, exact_ronsaku & lte_salesstartdate\
                & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')
            else:
                # カテゴリ〇文字〇の時
                # (選択したカテゴリと同じカテゴリに設定した商品データのなかで、
                # かつ入力した文字を含む商品データ)
                goods_search_result = GoodsTBL.objects.select_related()\
                .filter(exact_cate, exact_ronsaku\
                & (contains_name | contains_color | contains_price | contains_size)\
                & lte_salesstartdate & (gt_salesenddate | exact_salesenddate))\
                .order_by('-salesstartdate')

            # 1-4
            # 1-3で作成された検索結果goods_search_resultをfor文で回し、
            # 製品番号が表示用リスト(result_list)に格納されている。
            # 製品番号と被っていなければ、表示用リスト(result_list)にクエリオブジェクトを追加する処理
        result_list = []
        for loop in goods_search_result:
            productno_list = [d.productno for d in result_list]
            if loop.productno in productno_list:
                pass
            else:
                result_list.append(loop)

        context['result_list'] = result_list
        return context


class DetailsList(generic.ListView):
    """
    詳細画面のクラス
    ※結合するタイミングで削除するクラス
    """
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    template_name = 'searchapp/details.html'
