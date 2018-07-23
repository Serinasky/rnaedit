from django.shortcuts import render
from ..models import Sample, LevelLite, Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import copy

#此function是用來呼叫各個site有哪些sample而這些sample在這些site裡的A,G數量
def editing_detail(request):
    if request.GET["button"] == "editing_level":  # 單一點資料
        si = Site.objects.get(chromo=request.GET['chr'], loc=request.GET['site'])
        sam = Sample.objects.get(sample_barcode=request.GET['sample_barcode_field'])
        #從資料庫中抓取這個Sample在點選的這一點的Level
        sample_editing_level_module = LevelLite.objects.filter(site=si, sample=sam)
        #將抓出來的東西放入list以方便在前端進行操作
        level = sample_editing_level_module[0]
        #在此計算editing freq並將數值儲存進list
        if (level.redi_A + level.redi_G) != 0:
            ori_level = round(level.redi_G / (level.redi_A + level.redi_G), 2)
        else:
            ori_level = 0
        #將篩選好的資料回傳給前端的html
        return render(request, "level_details.html",\
        {"chromosome": request.GET["chr"], "site": request.GET["site"],\
        "level": level, "button": request.GET["button"], 'ori_level': ori_level, 
        'sam': sam})
    #此按鈕為有多少sample覆蓋到此點的數量的按鈕，若使用者點選此案鈕則執行以下程序
    else:  # request.GET["button"] == "edited_in"
        search_request_dict = copy.deepcopy(request.GET)
        # 一開始點選此按鈕並沒有回傳頁碼變數，所以預設為第一頁
        try:
            page = int(request.GET["page"])
        except:
            page = 1
        # 從資料庫將此點的Level全部抓出來
        target_site = request.GET["site"]
        if not request.GET["site"].endswith('-'):
            target_site = target_site[:-1] + '+'
        editing_level_module_list = LevelLite.objects.filter(site=target_site)
        try:
            current_sort = request.GET["current_sort"]
        except:
            current_sort = "editing_freq"
        try:
            sorted_direction = request.GET["sorted_direction"]
        except:
            sorted_direction = "up"

        if "click_sort" in request.GET:
            if current_sort == request.GET["click_sort"]:
                if sorted_direction == "down":
                    if request.GET["click_sort"] == "editing_freq":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G / (n.redi_A + n.redi_G + 1), reverse=True)
                    elif request.GET["click_sort"] == "total_freq":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: (n.redi_G + n.hyper_G) / (n.redi_A + n.redi_G + n.hyper_A + n.hyper_G), reverse=True)
                    elif request.GET["click_sort"] == "total_A":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A + n.hyper_A, reverse=True)
                    elif request.GET["click_sort"] == "total_G":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G + n.hyper_G, reverse=True)
                    elif request.GET["click_sort"] == "normal_A":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A, reverse=True)
                    elif request.GET["click_sort"] == "redi_G":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G, reverse=True)
                    else:
                        editing_level_module_list = editing_level_module_list.order_by("-sample__" + request.GET["click_sort"])
                    search_request_dict["sorted_direction"] = "up"
                else:
                    if request.GET["click_sort"] == "editing_freq":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G / (n.redi_A + n.redi_G + 1))
                    elif request.GET["click_sort"] == "total_freq":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: (n.redi_G + n.hyper_G )/ (n.redi_A + n.redi_G + n.hyper_A + n.hyper_G))
                    elif request.GET["click_sort"] == "total_A":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A + n.hyper_A)
                    elif request.GET["click_sort"] == "total_G":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G + n.hyper_G)
                    elif request.GET["click_sort"] == "normal_A":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A)
                    elif request.GET["click_sort"] == "redi_G":
                        editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G)
                    else:
                        editing_level_module_list = editing_level_module_list.order_by("sample__" + request.GET["click_sort"])
                    search_request_dict["sorted_direction"] = "down"
            else:
                if request.GET["click_sort"] == "editing_freq":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G / (n.redi_A + n.redi_G + 1))
                elif request.GET["click_sort"] == "total_freq":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: (n.redi_G + n.hyper_G )/ (n.redi_A + n.redi_G + n.hyper_A + n.hyper_G))
                elif request.GET["click_sort"] == "total_A":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A + n.hyper_A)
                elif request.GET["click_sort"] == "total_G":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G + n.hyper_G)
                elif request.GET["click_sort"] == "normal_A":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A)
                elif request.GET["click_sort"] == "redi_G":
                    editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G)
                else:
                    editing_level_module_list = editing_level_module_list.order_by("sample__" + request.GET["click_sort"])
                search_request_dict["sorted_direction"] = "down"
            search_request_dict["current_sort"] = request.GET["click_sort"]
        else:
            if current_sort == "editing_freq":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G / (n.redi_A + n.redi_G + 1))
            elif current_sort == "total_freq":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: (n.redi_G + n.hyper_G)/ (n.redi_A + n.redi_G + n.hyper_A + n.hyper_G))
            elif current_sort == "total_A":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A + n.hyper_A)
            elif current_sort == "total_G":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G + n.hyper_G)
            elif current_sort == "normal_A":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_A)
            elif current_sort == "redi_G":
                editing_level_module_list = sorted(editing_level_module_list, key=lambda n: n.redi_G)
            else:
                editing_level_module_list = editing_level_module_list.order_by("sample__" + current_sort)
            search_request_dict["sorted_direction"] = "up"
            search_request_dict["current_sort"] = current_sort
        
        #將資料轉換成list以利前端操作
        editing_details_list = list()
        #儲存sample barcode的set，用來給使用者在table裡當作篩選的清單
        sample_name_set = set()
        #儲存cancer type的set，用來給使用者在table裡當作篩選的清單
        cancer_type_set = set()
        #儲存tissue的set，用來給使用者在table裡當作篩選的清單
        tissue_set = set()
        #儲存body site的set，用來給使用者在table裡當作篩選的清單
        body_site_set = set()
        #將資料載入set當中
        for x in editing_level_module_list:
            editing_details_list.append([x.sample, x])
            sample_name_set.add(x.sample.sample_barcode)
            cancer_type_set.add(x.sample.cancer_type)
            tissue_set.add(x.sample.tumor_tissue_site)
            body_site_set.add(x.sample.tumor_tissue_site)
        if "sample_barcode_dropdown" in request.GET and len(request.GET["sample_barcode_dropdown"]) != 0:
            editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].sample_barcode == request.GET["sample_barcode_dropdown"])
        if "cancer_type_dropdown" in request.GET and len(request.GET["cancer_type_dropdown"]) != 0:
            editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].cancer_type == request.GET["cancer_type_dropdown"])
        if "tissue_dropdown" in request.GET and len(request.GET["tissue_dropdown"]) != 0:
            editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["tissue_dropdown"])
        if "body_site_dropdown" in request.GET and len(request.GET["body_site_dropdown"]) != 0:
            editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["body_site_dropdown"])
        #在此計算editing freq並將數值儲存進list
        for i, x in enumerate(editing_details_list):
            try:
                editing_details_list[i].append(x[1].redi_G / (x[1].redi_A + x[1].redi_G))
            except:
                editing_details_list[i].append(0)
            try:
                editing_details_list[i].append(x[1].hyper_G / (x[1].hyper_A + x[1].hyper_G))
            except:
                editing_details_list[i].append(0)

        
        #將多筆資料作成分頁，每10筆資料一頁
        try:
            datas_per_page = int(request.GET["datas_per_page"])
        except:
            datas_per_page = 50

        paginator = Paginator(editing_details_list, datas_per_page)

        try:
            editing_details_list = paginator.page(page)
        except PageNotAnInteger:
            editing_details_list = paginator.page(1)
        except EmptyPage:
            editing_details_list = paginator.page(paginator.num_pages)
        #將使用者搜尋的條件記錄起來，以利在選擇其他分頁時知道是以什麼搜尋條件去找那筆資料的第幾頁
        search_record = list()
        for key in search_request_dict:
            if key != "page":
                search_record.append(key + "=" + search_request_dict[key])
        search_record = "&".join(search_record)
        #將整理好的資料回傳給前端
        return render(request, "editing_details.html",\
        {"chromosome": '', "site": target_site,\
        "editing_details_list": editing_details_list, "search_record": search_record,\
        "search_request_dict": search_request_dict,\
        "sample_name_set": sample_name_set,\
        "cancer_type_set": cancer_type_set,\
        "tissue_set": tissue_set,\
        "body_site_set": body_site_set,\
        "button": request.GET["button"],"datas_per_page": datas_per_page,\
        "sorted_direction": sorted_direction, "current_sort": search_request_dict["current_sort"]})