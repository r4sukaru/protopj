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
            context = super().get_context_data(**kwargs)
        # template_nameは利用するテンプレート名
        #template_name = 'searchapp/result.html'

           #②-3(taguchi)
         #セッションの中にユーザの入力値が入っているかどうかの判定
         #↑（検索押した後に動いているので基本的にはなにかしら入ってる：Nullではない）
         #入っている場合は変数form_valueの中に②-2でユーザ入力値を格納したセッションを格納する
         #変数category_nameとsearch_charにユーザの入力値を格納する
         #↑（リストform_valueの番号を指定）
            '''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            category_name=form_value[0]
            search_char=form_value[1]
            #print(self.request.session['form_value'])
            '''
            #前画面フォームの代わりに全件検索用（カテゴリ、フォーム値なしの場合）
            form_value = ['','']
            category_name=form_value[0]
            search_char=form_value[1]

            #②-4(taguchi)
            #Qオブジェクトを作成。
            q_cate=Q(categoryid__exact=category_name)
            q_name=Q(goodsname__contains=search_char)
            q_color=Q(colorname__contains=search_char)
            q_price=Q(price__contains=search_char)
            q_size=Q(sizename__contains=search_char)
            q_ronsaku=Q(deleteflag__exact=0)

            #②-5(taguchi)
            #入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
            #分岐先で指定のクエリセットを発行し、変数goods_search_resultの中に格納する
            if (
                form_value[0:1]==['']
                ):
                if (
                    form_value[1:2]==['']):
                    #カテゴリ×文字×
                    goods_search_result =GoodsTBL.objects. \
                    filter(q_ronsaku).order_by('-salesstartdate')
                else:
                    #カテゴリ×文字〇
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter(q_name | q_color | q_price | q_size)\
                    .order_by('-salesstartdate')
            else:
                if form_value[1:2]==['']:
                    #カテゴリ〇文字×
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter(q_cate,q_ronsaku)\
                    .order_by('-salesstartdate')
                else:
                    #カテゴリ〇文字〇
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter( q_cate, ( q_name | q_color | q_price | q_size))\
                    .order_by('-salesstartdate')
                    #print(goods_search_result)

            #②-6(taguchi)
            #②-5で作成された検索結果goods_search_resultを
            #for文で回し、製品番号が表示用リストに格納されている
            #製品番号と被っていなければ、表示用リストにクエリオブジェクトを追加する処理

            result_list=[]
            for k in goods_search_result:
                productno_list=[d.productno for d in result_list]
                b=k.productno
                #print(k.categoryid.categoryname)
                if b in productno_list:
                    pass
                else:
                    result_list.append(k)

            context['result_list'] = result_list
            return context


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