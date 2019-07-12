from django.shortcuts import render
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
''
#class Search(generic.ListView):

    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    #model = GoodsTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    #template_name = 'searchapp/search.html'

    #def post(self, request, *args, **kwargs):
        #"""
       # 検索フォームに入力された値をセッションに格納するメソッド
       # ⇒初期アクセスでは、検索フォームに入力されていない⇒セッションに格納される処理は呼ばれない
        #⇒初期アクセスではこのメソッドは呼ばれない
        #"""
        # 検索値を格納するリストを新規作成
        #form_value = [
                #self.request.POST.get('title', None),
                #self.request.POST.get('category', None),
                #self.request.POST.get('price', None),
            #]

        # 検索値を格納するリストをセッションで管理する
        #request.session['form_value'] = form_value

        #'''
        #self.request.GET = self.request.GET.copy()
        #self.request.GET.clear()
        #'''

        # generic/list.pyのget()メソッドが呼び出される
        #return self.get(request, *args, **kwargs)

    #def get_context_data(self, **kwargs):
        #"""
         #初期値に空白を設定したテンプレートを返すメソッド
         #⇒最初にサイトを呼び出すときに必ず呼ばれる
        #"""
        # 親クラスのメソッド呼び出し、変数contextに格納
        #context = super().get_context_data(**kwargs)

        #title = ''
        #category = ''
        #price = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        #if 'form_value' in self.request.session:
            #form_value = self.request.session['form_value']
            #title = form_value[0]
            #category = form_value[1]
            #price = form_value[2]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        #default_data = {'title' :title, 'category' :category, 'price' :price}

        # 入力フォームに初期値では空白を設定する処理
        #test_form = GoodSearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        #context['test_form'] = test_form
        #return context

    #def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
        #'''
        #DBから検索条件に一致したデータを取得
       # '''
        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
       # if 'form_value' in self.request.session:
           # form_value = self.request.session['form_value']
            #title = form_value[0]
            #category = form_value[1]
            #price = form_value[2]

            #Qオブジェクトを各変数にインスタンス化
            #condition_title = Q()
            #condition_category = Q()
            #condition_price = Q()

            # クエリを発行
            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
            #if len(title) != 0 and title[0]:
                #condition_title = Q(title__contains = title)
            #if len(category) != 0 and category[0]:
                #condition_category = Q(category__contains = category)
           # if len(price) != 0 and price[0]:
               # condition_price = Q(price__contains = price)

            # 定義されたクエリを発行し、データをobject_listへ格納する。
            #return GoodsTBL.objects.select_related().all()

        #else:
            #return GoodsTBL.objects.none() # 何も返さない


class ResultList(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    model = GoodsTBL

    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/result.html'

    def post(self, request, *args, **kwargs):
        #テンプレート内のformタグで
            print (request.POST)
            if request.method == 'post':
                form = 'yes'
                #sizeform(request.post)
            else:
                form = 'no'
                #form = sizeform()

            #return render(request,'searchapp/details.html',{'form': form})
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

            # 親クラスのメソッド呼び出し、変数contextに格納
            context = super().get_context_data(**kwargs)

            goodsid = 'AABBCC001S003'
            productno = goodsid[:9]
            deleteflag = 0 # 有効状態

            '''
            ■DB検索条件
            製品番号 = 'ZZYYXX001'
            論理削除フラグ = 0
            販売開始年月日 ≦システム処理何月日＜販売終了年月日
            '''
              # Qオブジェクトの初期設定(インスタンス化)
            exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
            exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
            exact_deleteflag = Q() # 論理削除フラグのQオブジェクト(完全一致)

            #インスタンス化した変数にQオブジェクト(検索条件)を記述
            exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='ZZYYXX001S003'
            exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='ZZYYXX001'
            exact_deleteflag = Q(deleteflag__exact = int(deleteflag))  # 条件：論理削除フラグ = 1

            # Qオブジェクトで定義した検索条件でクエリを発行する。
            goodsdetail = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_productno)
            pdfull = GoodsTBL.objects.select_related().filter(exact_productno)

            # contextにクエリ発行した結果を追加し、テンプレートタグで使用可能にする。
            context['goods_form'] = goodsdetail

            # 戻り値としてcontextを返す。
            return context

    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
            '''
            詳細画面に表示する商品を検索する。
            '''
            goodsid = 'AABBCC001S003'
            productno = goodsid[:9]
            deleteflag = 0 # 有効状態
            '''
            ■DB検索条件
            製品番号 = 'ZZYYXX001'
            論理削除フラグ = 0
            販売開始年月日 ≦システム処理何月日＜販売終了年月日
            '''
            #Qオブジェクトを各変数にインスタンス化
            condition_goodsid = Q() #商品IDのQオブジェクト(含め)
            exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
            exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
            condition_salesstartdate = Q() # 販売開始年月日のQオブジェクト(含め)
            condition_salesenddate = Q() # 販売終了年月日のQオブジェクト(含め)
            exact_deleteflag = Q() #論理削除フラグのQオブジェクト(完全一致)

            # クエリを発行
            exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
            condition_goodsid = Q(goodsid__contains = str(productno)) # 条件：商品IDに'AABBCC001'が含まれている
            exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
            exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1

            shousai = GoodsTBL.objects.select_related().filter(exact_goodsid & exact_productno & exact_deleteflag)
            #print(GoodsTBL.objects.select_related().filter(exact_goodsid & exact_productno & exact_deleteflag)
            # 定義されたクエリを発行し、データをgoodsdetailsへ格納する。
            return shousai

            #return redirect('post_detail', pk=post.pk)

class Details_view(generic.ListView):
     #modelは取り扱うモデルクラス(モデル名と紐づけ)
     model = GoodsTBL
     #template_nameは利用するテンプレート名
     template_name = 'searchapp/details.html'

     def post_details(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'searchapp/details.html', {'post': post})