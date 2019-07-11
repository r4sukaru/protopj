from django.shortcuts import render
from django.views import generic
from .forms import GoodSearchForm
from django.db.models import Q
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL
from django.views.generic.base import TemplateView
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
    #model = CategoryTBL
    # template_nameは利用するテンプレート名
    # (ListViewの場合、何も設定しないとhtml名の最後に[_list]が付く)
    template_name = 'searchapp/result.html'

def get_context_data(self, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        context = super().get_context_data(**kwargs)

        productno = ''
        categoryidid = ''
        highcategoryidid = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            productno = form_value[0]
            categoryid = form_value[1]
            highcategoryidid = form_value[2]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        default_data = {'productno' :productno, 'categoryid' :categoryid, 'highcategoryidid' :highcategoryidid}

        # 入力フォームに初期値では空白を設定する処理
        test_form = GoodSearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['test_form'] = test_form
        return context

def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
        '''
        DBから検索条件に一致したデータを取得
        '''
        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            productno = form_value[0]
            categoryid = form_value[1]
            highcategoryidid = form_value[2]

            #Qオブジェクトを各変数にインスタンス化
            condition_productno = Q()
            condition_categoryid = Q()
            condition_highcategoryidid = Q()

            # クエリを発行
            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
            if len(productno) != 0 and productno[0]:
                condition_productno = Q(productno__contains = productno)
            if len(categoryid) != 0 and categoryid[0]:
                condition_categoryid = Q(categoryid__contains = categoryid)
            if len(highcategoryidid) != 0 and highcategoryidid[0]:
                condition_highcategoryidid = Q(highcategoryidid__contains = highcategoryidid)

            # 定義されたクエリを発行し、データをobject_listへ格納する。
            #return GoodsTBL.objects.select_related().filter(condition_productno & condition_categoryid & condition_highcategoryidid)
            return GoodsTBL.objects.select_related().filter(condition_productno)

#class Details_view(generic.ListView):
    # modelは取り扱うモデルクラス(モデル名と紐づけ)
    #model = GoodsTBL
    # template_nameは利用するテンプレート名
    #template_name = 'searchapp/details.html'

    #def post_details(request, pk):
        #post = get_object_or_404(Post, pk=pk)
        #return render(request, 'searchapp/details.html', {'post': post})