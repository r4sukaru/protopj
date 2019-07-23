from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from .forms import GoodSearchForm
from django.db.models import Q
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404


# Create your views here.

class Search(generic.ListView):

    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    # template_nameは利用するテンプレート名
    template_name = 'searchapp/search.html'


class ResultList(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL

    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        print(request.POST.get('productno',None))
        request.session['g_de_productno'] = request.POST.get('productno',None)

        return redirect('searchapp:details')

    def get_context_data(self, **kwargs):

            # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        goodsid = '000000006L002'
        productno = goodsid[:9]
        deleteflag = 0 # 有効状態

        #■DB検索条件
        #製品番号 = 'ZZYYXX001'
        #論理削除フラグ = 0
        #販売開始年月日 ≦システム処理何月日＜販売終了年月日

        # Qオブジェクトの初期設定(インスタンス化)
        exact_goodsid = Q() # 商品IDのQオブジェクト(exact=完全一致）
        exact_productno = Q() # 製造番号のQオブジェクト(exact=完全一致)
        exact_deleteflag = Q() # 論理削除フラグのQオブジェクト(exact=完全一致)


        #インスタンス化した変数にQオブジェクト(検索条件)を記述
        exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='ZZYYXX001S003'
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='ZZYYXX001'
        exact_deleteflag = Q(deleteflag__exact = int(deleteflag))  # 条件：論理削除フラグ = 1

        # Qオブジェクトで定義した検索条件でクエリを発行する。
        goodsresult = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_productno & exact_deleteflag)
        #pdfull = GoodsTBL.objects.select_related().filter(exact_productno)

        # contextにクエリ発行した結果を追加し、テンプレートタグで使用可能にする。
        context['goods_form'] = goodsresult

        # 戻り値としてcontextを返す。
        return context

    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）

            #詳細画面に表示する商品を検索する。

        goodsid = '000000006L002'
        productno = goodsid[:9]
        deleteflag = 0 # 有効状態

        #■DB検索条件
        #製品番号 = 'ZZYYXX001'
        #論理削除フラグ = 0
        #販売開始年月日 ≦システム処理何月日＜販売終了年月日

        #Qオブジェクトを各変数にインスタンス化
        condition_goodsid = Q() #商品IDのQオブジェクト(condition=含め)
        exact_goodsid = Q() # 商品IDのQオブジェクト(exact=完全一致)
        exact_productno = Q() # 製造番号のQオブジェクト(exact=完全一致)
        condition_salesstartdate = Q() # 販売開始年月日のQオブジェクト(condition=含め)
        condition_salesenddate = Q() # 販売終了年月日のQオブジェクト(condition=含め)
        exact_deleteflag = Q() #論理削除フラグのQオブジェクト(exact=完全一致)

        # クエリを発行
        exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
        condition_goodsid = Q(goodsid__contains = str(productno)) # 条件：商品IDに'AABBCC001'が含まれている
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1

        shousai = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_productno & exact_deleteflag)
        #print('shousai = ' +str(shousai))

        for data in shousai:
            #print('shousai = ' +(data.productno))
            self.request.session['seino'] = data.productno
            break

        #aa = self.request.session['seino']
        #print(aa)

        # 定義されたクエリを発行し、データをgoodsdetailsへ格納する。
        return shousai

    #def redirectview(request):

        #return redirect('details')

class DetailsList(generic.ListView):
    #modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL
    #template_nameは利用するテンプレート名
    template_name = 'searchapp/details.html'

    def post_details(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'searchapp/details.html', {'post': post})


    def post(self, request, *args, **kwargs):
        #テンプレート内のformタグで
            print (request.POST)
            if request.method == 'post':
                print('post')
            else:
                form = 'no'

            #return render(request,'searchapp/details.html',{'form': form})
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

            # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)