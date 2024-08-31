import time

import flet
import re
import warnings
import pickle
from time import sleep
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import flet as ft
from googletrans import Translator
translator=Translator()
warnings.filterwarnings('ignore')
symptoms_set = pd.read_csv("assets/file.csv")
specialist_set = pd.read_excel("assets/Data.xlsx")
doctors_set = pd.read_excel("assets/doctors.xlsx")
doctors_set['Telephone1']=doctors_set['Telephone1'].fillna('No Phone Availiable')
train_set=pd.read_csv("assets/Training.csv")
test_set=pd.read_csv("assets/Testing.csv")

doctors_list=[]
check_boxes_list=[]
def main(page:ft.Page):
    page.fonts={
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"

    }
    page.theme = ft.Theme(font_family="Kanit",color_scheme_seed="red")
    page.title="Doctor's Assistant"
    page.theme_mode = 'dark'
    search_image=ft.Image( border_radius=80,width=300,height=300,fit=ft.ImageFit.FIT_HEIGHT)
    def cancelErrorText(e):
        search_text.error_text=None
        page.update()
    def cancelErrorText2(e):
        search_text2.error_text=None
        search_text2.suffix=ft.Row([
            search_button,
            filter_button
        ],width=85)
        search_text2.suffix_icon=None
        page.update()
    # ADD PROGESSBAR EFFECT WHEN CHANGE LIGHT OR DARK
    # THIS OPTIONAL
    switch_language=ft.RadioGroup(ft.Column([
        ft.Radio(value='Arabic',label='Arabic'),
        ft.Radio(value='english', label='english')
    ]),value='Arabic')
    def dismiss_dlg2(e):
        dlg.open=False
        page.update()
    page.splash = ft.ProgressBar(visible=False)
    description_text = ft.Text("This is a graduation project for the faculty of computer and information science-Ain shams university that diagnoses disease cases by symptoms.",weight=ft.FontWeight.BOLD)
    create_text=ft.Text("Created by :", weight=ft.FontWeight.W_900)
    name1 = ft.Text("Abdelrahman Ali Ahmed", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    name2 = ft.Text("Ahmed Emam Mohamed", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    name3 = ft.Text("Omar Khaled Elsayed", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    name4 = ft.Text("Mahmoud Ahmed Gaber", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    name5 = ft.Text("Ahmed Mohamed Hussien", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    supervision_text=ft.Text("Under Supervision of :", weight=ft.FontWeight.W_900)
    doctor_name=ft.Text("Dr. Dina Elsayad", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    doctor_title= ft.Text("(lecturer at Faculty of Computer and Information Science, Scientific Computing Department )", color=ft.colors.GREEN,font_family=ft.TextThemeStyle.TITLE_SMALL,size=20)
    TA_name= ft.Text("TA. Rezq Muhammed ", color=ft.colors.GREEN, weight=ft.FontWeight.W_900)
    TA_Title=ft.Text("(Teaching Assistant at Faculty of Computer and Information Science, Ain Shams University)", color=ft.colors.GREEN,font_family=ft.TextThemeStyle.TITLE_SMALL,size=20)
    dlg = ft.AlertDialog(
        title=ft.Column([
            description_text,

            ft.Row([
                ft.Column([
                ft.Text(""),
                create_text,
                name1,
                name2,
                name3,
                name4,
                name5
            ]
            ), ft.Column([
                supervision_text,
                doctor_name,
                doctor_title,
                TA_name,
                TA_Title,



            ])],spacing=160)

        ])
    ,on_dismiss=dismiss_dlg2)
    def search_without_filter(e):

        if search_text2.value=='':
            if switch_language.value=='english':
                search_text2.error_text = "Enter doctor's name please"
            else:
                search_text2.error_text = "برجاء ادخال اسم الطبيب"
            page.update()
        else:
            search_results_list.append(list(doctors_set[doctors_set['مقدم الخدمة :'].str.contains(search_text2.value)].values))
            page.go('/search')
    def open_dlg2(e):
        search_text.value=search_text2.value
        search_text2.value=None
        search_text2.error_text=None
        dropdown2.value='None'
        dropdown.value='None'
        search_results_list.clear()
        search_results_list2.clear()
        selected_govern.clear()
        selected_specialty.clear()
        tag_list2.controls.clear()
        tag_list.controls.clear()
        dropdown.counter_text = None
        dropdown2.counter_text = None
        page.dialog = dlg2
        dlg2.open = True
        page.update()

    filter_button = ft.IconButton(icon=ft.icons.FILTER_LIST, on_click=open_dlg2, tooltip='advanced search')
    search_results_list2 = []
    search_results_list = []


    def search_with_filter(e):

        if selected_specialty==[] and selected_govern==[]:
            if switch_language.value=='english':
                dropdown.error_text = "Please Choose Filter !!"
                dropdown2.error_text = "Please Choose Filter !!"
            else:
                dropdown.error_text = "لم تقم بالاختيار !!"
                dropdown2.error_text = "لم تقم بالاختيار !!"

            page.update()
            return
        elif search_text.value=='' and selected_specialty!=[] and selected_govern==[]:
            search_results_list2.append(list(doctors_set[doctors_set['التخصص :'].isin(selected_specialty)].values))
        elif search_text.value=='' and selected_specialty==[] and selected_govern!=[]:
            search_results_list2.append(list(doctors_set[doctors_set['المحافظة '].isin(selected_govern)].values))
        elif search_text.value=='' and selected_specialty!=[] and selected_govern!=[]:
            search_results_list2.append(list(doctors_set[(doctors_set['المحافظة '].isin(selected_govern))&(doctors_set['التخصص :'].isin(selected_specialty))].values))



        elif search_text.value!='' and selected_specialty!=[] and selected_govern==[]:
            search_results_list2.append(list(doctors_set[(doctors_set['التخصص :'].isin(selected_specialty))&(doctors_set['مقدم الخدمة :'].str.contains(search_text.value))].values))
        elif search_text.value!='' and selected_specialty==[] and selected_govern!=[]:
            search_results_list2.append(list(doctors_set[(doctors_set['المحافظة '].isin(selected_govern))&(doctors_set['مقدم الخدمة :'].str.contains(search_text.value))].values))
        elif search_text.value!='' and selected_specialty!=[] and selected_govern!=[]:
            search_results_list2.append(list(doctors_set[(doctors_set['المحافظة '].isin(selected_govern))&(doctors_set['التخصص :'].isin(selected_specialty))&(doctors_set['مقدم الخدمة :'].str.contains(search_text.value))].values))
        dlg2.open=False
        dlg2.update()
        page.go('/Advanced-search')





    search_text=ft.TextField(label='enter doctor name',
                 visible=True, width=300,value='',on_focus=cancelErrorText,on_submit=search_with_filter,color=ft.colors.WHITE,bgcolor=ft.colors.BLACK,border_color=ft.colors.BLUE_300,border_width=5)

    governorates_list = list(doctors_set['المحافظة '].unique())
    Specialties_list = list(doctors_set['التخصص :'].unique())
    dropdown = ft.Dropdown(width=500, label="Governorate", hint_text="Select governorate",value='None',height=100,border_color=ft.colors.BLUE_300,border_width=5)
    dropdown2 = ft.Dropdown(width=500, label="Specialty", hint_text="Select specialty",value='None',height=100,border_color=ft.colors.BLUE_300,border_width=5)



    selected_govern=[]
    selected_specialty=[]

    def delete_tag(e):

        for index, row_item in enumerate(tag_list.controls):
            if e.control.data == row_item.controls[0].text:
                break
        selected_govern.pop(index)
        tag_list.controls.pop(index)  # Pop the tag out of the list.
        if len(selected_govern)==0:
            dropdown.counter_text=None
        else:
            dropdown.counter_text = "Tag Count: %s" % len(selected_govern)  # Update counter.
        page.update()  # Update page.

    def add_tag(e):
        exists=False
        t = dropdown.value
        dropdown.value="None"
        dropdown.update()
        for tag in selected_govern:
            if t==tag:
                exists=True
                break
        if exists==False:
                dropdown.error_text=None
                dropdown2.error_text=None
                selected_govern.append(t)

                t1 = re.sub(r'[0-9]', '', t)
                t1 = t1.strip('()')
                t1 = t1.strip(' ')
                t1=translator.translate(t1,dest='en')

                del_btn = ft.ElevatedButton(text=t1.text, icon=ft.icons.CLOSE_OUTLINED, on_click=delete_tag, data=t,
                                            icon_color=ft.colors.BLUE_300, color=ft.colors.BLUE_300, bgcolor=ft.colors.BLACK)
                if switch_language.value=='Arabic':
                    del_btn.text=t1.origin
                if toggledarklight.selected == True:
                    del_btn.bgcolor=ft.colors.WHITE
                else:
                    del_btn.bgcolor=ft.colors.BLACK
                tag_list.controls.append(ft.Column(controls=[del_btn]))
                dropdown.counter_text = "Tag Count: %s" % len(selected_govern)
                # Update counter.
                page.update()  # Update page.
        else:
            dropdown.error_text="Chosen Once"
            page.update()

        page.update()
    def delete_tag2(e):

        for index, row_item in enumerate(tag_list2.controls):
            if e.control.data == row_item.controls[0].text:
                break
        selected_specialty.pop(index)
        tag_list2.controls.pop(index)  # Pop the tag out of the list.
        if len(selected_specialty)==0:
            dropdown2.counter_text=None
        else:
            dropdown2.counter_text = "Tag Count: %s" % len(selected_specialty)  # Update counter.
        page.update()  # Update page.

    def add_tag2(e):
        exists = False
        t = dropdown2.value
        dropdown2.value="None"
        for tag in selected_specialty:
            if t == tag:
                exists = True
                break
        if exists == False:
            dropdown.error_text = None
            dropdown2.error_text = None
            selected_specialty.append(t)
            t = translator.translate(t, dest='en')
            del_btn = ft.ElevatedButton(text=t.text, icon=ft.icons.CLOSE_OUTLINED, on_click=delete_tag2, data=t,
                                        icon_color=ft.colors.BLUE_300, color=ft.colors.BLUE_300,
                                        bgcolor=ft.colors.BLACK)
            if switch_language.value == 'Arabic':
                del_btn.text = t.origin
            if toggledarklight.selected == True:
                del_btn.bgcolor = ft.colors.WHITE
            else:
                del_btn.bgcolor = ft.colors.BLACK
            tag_list2.controls.append(ft.Column(controls=[del_btn]))
            dropdown2.counter_text = "Tag Count: %s" % len(selected_specialty)  # Update counter.
            page.update()  # Update page.
        else:
            dropdown2.error_text = "Chosen once"
            page.update()

        page.update()
    dropdown.on_change=add_tag
    dropdown2.on_change=add_tag2
    tag_list = ft.Row(wrap=True,width=500)
    tag_list2 = ft.Row(wrap=True,width=500)
    def dismiss_dlg(e):
        search_text.value = None
        dropdown.value = 'None'
        dropdown2.value = 'None'
        search_text.error_text = None
        dropdown2.error_text=None
        dropdown.error_text=None
        tag_list.controls.clear()
        tag_list2.controls.clear()
        selected_govern.clear()
        selected_specialty.clear()
        dropdown.counter_text=None
        dropdown2.counter_text=None
        dlg2.open = False
        page.update()


    search_image.src=f"1.gif"
    advanced_search_icon= ft.FloatingActionButton(content=search_image,tooltip='Search', on_click=search_with_filter,bgcolor=ft.colors.BLACK,width=100,height=100,shape=ft.CircleBorder())
    advanced_search_text = ft.Text('Advanced Search', font_family=ft.FontWeight.W_900, size=35)

    cont=ft.Container(content=ft.Row([ft.Column([
        ft.Row([ft.IconButton(ft.icons.CLOSE, on_click=dismiss_dlg),
                ft.Row([
                    advanced_search_text

                ])
                ], spacing=550),

            ft.Column([
                ft.Row(
                    [
                        search_text,

                    ]
                ),
            dropdown2,
            tag_list2,
            dropdown,
            tag_list])

    ]),ft.VerticalDivider(width=1,color=ft.colors.TRANSPARENT),
      advanced_search_icon,
    ],spacing=50), bgcolor=ft.colors.BLACK,width=700,height=500)
    dlg2=ft.BottomSheet(
        content=ft.ListView(controls=[cont],expand=True),
        on_dismiss=dismiss_dlg
    )


    def search(e):
        AB.title=txt1
        if toggledarklight.selected:
            search_text2.bgcolor=ft.colors.WHITE
            search_text2.color=ft.colors.BLACK
        else:
            search_text2.bgcolor=ft.colors.BLACK
            search_text2.color=ft.colors.WHITE
        AB.leading=ft.IconButton(icon=ft.icons.CANCEL,on_click=CancelSearching,tooltip='Cancel')
        if switch_language.value=='Arabic':
            AB.leading.tooltip='الغاء'
        search_text2.autofocus=True
        page.update()
    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()


    def wait(e):
        loading_text=ft.Text("Please wait untill the page complete loading !!! ")
        if switch_language.value=='Arabic':
            loading_text.value='برجاء الانتظار حتي يكتمل التحميل'
        page.snack_bar = ft.SnackBar(loading_text)
        page.snack_bar.open = True
        page.update()
        return

    submit_button = ft.Icon(ft.icons.THUMB_UP)
    submit_text = ft.Text("Submit")

    reset_button=ft.Icon(ft.icons.LOCK_RESET_ROUNDED)
    reset_text=ft.Text("Reset")
    wait_massage=ft.Text("Please Wait..", style="headlineSmall", width=500, weight=ft.FontWeight.W_900,text_align='CENTER')

    nurse_image = ft.Image(width=500,src=f"nurse-2.jpg")

    c = ft.Container(content=ft.Column(
        [
            wait_massage,
            ft.ProgressBar(width=500, color="amber", bgcolor="#eeeeee"),
            nurse_image

        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=1000
    ), bgcolor=ft.colors.BLACK,width=2000,height=700)
    def changetheme(e):
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()
        # DELAY EFFECT THE ANIMATION
        sleep(0.5)
        # CHANGE THE ICON DARK MODE OR LIGHT MODE
        toggledarklight.selected = not toggledarklight.selected
        if toggledarklight.selected == True:
            if switch_language.value=='english':
                toggledarklight.tooltip = "Light Mode"
            else:
                toggledarklight.tooltip ='الوضع النهاري'

            submit_button.color = ft.colors.BLACK
            submit_text.color = ft.colors.BLACK
            reset_button.color = ft.colors.BLACK
            reset_text.color = ft.colors.BLACK
            search_text2.bgcolor=ft.colors.WHITE
            search_text2.color=ft.colors.BLACK
            search_image.src=f"search.gif"
            cont.bgcolor=ft.colors.WHITE
            nurse_image.src=f"nurse.jpg"
            c.bgcolor=ft.colors.WHITE
            search_text.bgcolor=ft.colors.WHITE
            search_text.color=ft.colors.BLACK
            search_image.border_radius=100
            advanced_search_icon.bgcolor=ft.colors.SURFACE
        else:
            if switch_language.value=='english':
                toggledarklight.tooltip = "Dark Mode"
            else:
                toggledarklight.tooltip ='الوضع المظلم'
            submit_button.color = ft.colors.WHITE
            submit_text.color = ft.colors.WHITE
            reset_button.color = ft.colors.WHITE
            reset_text.color = ft.colors.WHITE
            search_text2.bgcolor=ft.colors.BLACK
            search_text2.color=ft.colors.WHITE
            search_image.src=f"1.gif"
            cont.bgcolor=ft.colors.BLACK
            nurse_image.src=f"nurse-2.jpg"
            c.bgcolor=ft.colors.BLACK
            search_text.bgcolor=ft.colors.BLACK
            search_text.color=ft.colors.WHITE
            advanced_search_icon.bgcolor=ft.colors.BLACK

        # AND DISABLE AGAIN THE PROGRESSBAR WHEN CHANGE DARK MODE
        page.splash.visible = False

        # AND PAGE UPDATE FOR CHANGE STATE
        page.update()

    # CREATE TOGLE BUTTON DARK MODE LIGHT
    toggledarklight = ft.IconButton(
        on_click=changetheme,
        icon="dark_mode",
        selected_icon="light_mode",
        style=ft.ButtonStyle(
            # change color if light and dark
            color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}

        )


    )
    if toggledarklight.selected == True:
        if switch_language.value == 'english':
            toggledarklight.tooltip = "Light Mode"
        else:
            toggledarklight.tooltip = 'الوضع النهاري'
    else:
        if switch_language.value == 'english':
            toggledarklight.tooltip = "Dark Mode"
        else:
            toggledarklight.tooltip = 'الوضع المظلم'
    def button_clicked(e):
        list = []
        check=False
        for k in check_boxes_list:
            if k.value==True:
                check=True
        if check==False:
            select_text=ft.Text("Please choose your symptoms !!! ")
            if switch_language.value=='Arabic':
                select_text.value='برجاء اختيار الاعراض !!!'
            page.snack_bar = ft.SnackBar(select_text)
            page.snack_bar.open = True
            page.update()
            return
        for j in check_boxes_list:
             if j.value==True:
                 list.append(1)
             else:
                 list.append(0)
        page.update()
        dlist = [list]
        prediction = Model.predict(dlist)
        #prediction = [np.argmax(i) for i in prediction] #for ANN Model
        prediction = encoder.inverse_transform(prediction)
        pred=str(prediction).strip("['")
        pred=pred.strip("']")
        التخصص = specialist_set.loc[specialist_set['Diseases']==pred]['التخصص :'].values[0]
        doctors=doctors_set[doctors_set['التخصص :']== التخصص].values
        doctors_list=doctors.tolist()
        r2 = ft.Row(wrap=True, scroll='always', expand=True, width=2000, height=1000)
        def change_filter(e):
            b = False
            if db.value == 'None':
                b = True
            for j in doctors_list:
                if j[0] == db.value:
                    b = True
                    break
            if (b == True):
                tmp = []
                db.error_text = None
                if db.value != 'None':
                    for i in doctors_list:
                        if i[0] == db.value:
                            tmp.append(i)
                else:
                    tmp = doctors_list
                r2.controls.clear()
                for j in tmp:
                    phone = str(j[6]).replace('\n', ',')
                    phone = phone.replace('/', ',')
                    phone = phone.replace('-', ',')
                    phone = phone.replace('_', ',')
                    region = re.sub(r'[0-9]', '', j[0])
                    region = region.strip('()')
                    region = region.strip(' ')
                    details3 = ft.Column([
                        ft.Icon(ft.icons.MEDICAL_INFORMATION, size=80),
                        ft.Row([ft.Icon(ft.icons.PERSON, tooltip='Name', size=28),
                                ft.Text(value=j[4], weight=ft.FontWeight.BOLD, size=28)]),
                        ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='governorate', size=28),
                                ft.Text(value=region, weight=ft.FontWeight.BOLD, size=28)]),
                        ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='region', size=28),
                                ft.Text(value=str(j[1]), weight=ft.FontWeight.BOLD, size=28)]),
                        ft.Row([ft.Icon(ft.icons.GPS_FIXED, tooltip='address', size=28),
                                ft.Text(value=str(j[5]), weight=ft.FontWeight.BOLD, size=28)]),
                        ft.Row([ft.Icon(ft.icons.PHONE, tooltip='phone number(s)', size=28),
                                ft.Text(value=phone, weight=ft.FontWeight.BOLD, size=28)]),
                        ft.Row([ft.Icon(ft.icons.WORK, tooltip='specialization', size=28),
                                ft.Text(value=str(j[3]), weight=ft.FontWeight.BOLD, size=28)]),

                    ], alignment=ft.MainAxisAlignment.CENTER)

                    r2.controls.append(
                        ft.Container(
                            details3,
                            width=1020,
                            height=440,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREEN,
                            border=ft.border.all(1, ft.colors.BLACK),
                            border_radius=ft.border_radius.all(10),
                            padding=ft.padding.only(left=10)

                        )
                    )
                page.update()

            else:
                if switch_language.value == 'english':
                    db.error_text = 'Not avaliable yet'
                else:
                    db.error_text = 'غير متاح حاليا'
                page.update()
        db = ft.Dropdown(width=300, label="Select your governorate", hint_text="Select your governorate ", height=70,
                         border_color=ft.colors.BLUE_300, border_width=5, on_change=change_filter)
        pb = ft.ProgressBar(width=400)
        page.go('/loading')
        if page.route=='/loading':
            loading_text=ft.Text("Loading", size=30,weight=ft.FontWeight.W_900)
            if switch_language.value=='Arabic':
                loading_text.value='جار التحميل'
            bar=ft.AppBar(
                            title=loading_text,
                            bgcolor=ft.colors.GREEN_900,
                            leading=ft.IconButton(icon=ft.icons.DOWNLOADING,on_click=wait),
                            actions=[
                                collage_sign,
                                toggledarklight

                            ]
                        )

            page.horizontal_alignment=ft.CrossAxisAlignment.START
            page.vertical_alignment=ft.MainAxisAlignment.START
            page.views.append(
                flet.View(
                    "/loading",[
                        bar,
                        c,


                    ]
                )
            )
            page.update()
        opt = []
        None_option = ft.dropdown.Option("None")
        opt.append(None_option)
        governorates_list.sort(reverse=False)
        for governorates in governorates_list:
            region = re.sub(r'[0-9]', '', governorates)
            region = region.strip('()')
            region = region.strip(' ')

            if switch_language.value == 'english':
                region = translator.translate(region, dest='en')
                opt.append(ft.dropdown.Option(text=region.text, key=governorates))
            else:
                opt.append(ft.dropdown.Option(text=region, key=governorates))
        db.options = opt
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)

        if switch_language.value == 'Arabic':
            db.label = 'اختر محافظتك'
            db.hint_text = 'اختر محافظتك'


        specialist = specialist_set.loc[specialist_set['Diseases'] == pred]['Doctor Specialist'].values[0]
        page.go("/result")


        if page.route == "/result":



            for j in doctors_list:
                phone = str(j[6]).replace('\n', ',')
                phone = phone.replace('/', ',')
                phone = phone.replace('-', ',')
                phone = phone.replace('_', ',')
                region = re.sub(r'[0-9]', '', j[0])
                region = region.strip('()')
                region = region.strip(' ')
                details = ft.Column([
                    ft.Icon(ft.icons.MEDICAL_INFORMATION, size=80),
                    ft.Row([ft.Icon(ft.icons.PERSON, tooltip='Name', size=28),
                            ft.Text(value=j[4], weight=ft.FontWeight.BOLD, size=28)]),
                    ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='governorate', size=28),
                            ft.Text(value=region, weight=ft.FontWeight.BOLD, size=28)]),
                    ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='region', size=28),
                            ft.Text(value=str(j[1]), weight=ft.FontWeight.BOLD, size=28)]),
                    ft.Row([ft.Icon(ft.icons.GPS_FIXED, tooltip='address', size=28),
                            ft.Text(value=str(j[5]), weight=ft.FontWeight.BOLD, size=28)]),
                    ft.Row([ft.Icon(ft.icons.PHONE, tooltip='phone number(s)', size=28),
                            ft.Text(value=phone, weight=ft.FontWeight.BOLD, size=28)]),
                    ft.Row([ft.Icon(ft.icons.WORK, tooltip='specialization', size=28),
                            ft.Text(value=str(j[3]), weight=ft.FontWeight.BOLD, size=28)]),

                ], alignment=ft.MainAxisAlignment.CENTER)
                r2.controls.append(
                    ft.Container(
                        details,
                        width=1020,
                        height=440,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN,
                        border=ft.border.all(1, ft.colors.BLACK),
                        border_radius=ft.border_radius.all(10),
                        padding=ft.padding.only(left=10)

                    )
                )
            recommendation_text=ft.Text("Recommendation page", size=30,weight=ft.FontWeight.W_900)
            prediction_text=ft.Text(f"You May Have : {pred}", size=50, weight=ft.FontWeight.W_900, selectable=True, text_align='LEFT')
            recommendation_text2=ft.Text(f"You Should visit a {specialist} doctor", size=50, weight=ft.FontWeight.W_900, selectable=True,text_align='LEFT')
            recommendation_doctors_text = ft.Text(
                f"Suggested {specialist} Doctors : ",
                size=50,
                color=ft.colors.RED,
                weight=ft.FontWeight.BOLD,
                italic=True,
                text_align='LEFT'
            )
            if switch_language.value=='Arabic':
                recommendation_text.value='صفحة الاقتراحات'
                prediction_text.value=f" ربما يكون لديك : {translator.translate(pred,dest='ar').text}"
                recommendation_text2.value=f" يجب عليك زيارة دكتور {specialist_set.loc[specialist_set['Diseases']==pred]['التخصص :'].values[0]}"
                recommendation_doctors_text.value=f"  دكاترة ال{specialist_set.loc[specialist_set['Diseases']==pred]['التخصص :'].values[0]} المقترحين "
            page.views.append(
                flet.View(
                    "/result",
                    [
                        ft.AppBar(
                            title=recommendation_text,
                            bgcolor=ft.colors.GREEN_900,
                            leading=ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=view_pop,tooltip='Back'),
                            actions=[
                                collage_sign,
                                toggledarklight

                            ]
                        ),

                        prediction_text,

                        recommendation_text2,
                        ft.Row([recommendation_doctors_text
                            ,
                            db

                        ])
                        ,

                        r2


,

                    ],

                )
            )
        page.update()


    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            [submit_button, submit_text], alignment="CENTER", spacing=5
        ),
        bgcolor=ft.colors.GREEN_900,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
        on_click=button_clicked

    )




    def button_clicked_reset(e):
        check=False
        for k in check_boxes_list:
            if k.value==True:
                check=True
        if check==False:
            if switch_language.value=='english':
                page.snack_bar = ft.SnackBar(ft.Text("You didn't choose any symptoms yet !!! "))
            else:
                page.snack_bar = ft.SnackBar(ft.Text("انت لم تقم باختيار اي اعراض بعد !!! "))
            page.snack_bar.open = True
            page.update()
            return
        for j in check_boxes_list:
             if j.value==True:
                 j.value=False
        page.update()

    page.floating_reset_button = ft.FloatingActionButton(
        content=ft.Row(
            [reset_button, reset_text], alignment="CENTER", spacing=5
        ),
        bgcolor=ft.colors.GREEN_900,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
        on_click=button_clicked_reset
    )

    search_txt=ft.Text("Search")
    r2 = ft.Row(
        [
            ft.Icon(ft.icons.SEARCH),
            search_txt,


        ]
        ,visible=True
    )
    def dismiss_txt(e):
        search_text2.value = None
        search_text2.suffix=None
        search_text2.suffix_icon=ft.icons.SEARCH
        page.update()
    search_text2=ft.TextField(visible=True,width=500,value=None,height=50,cursor_radius=30,cursor_height=25,on_submit=search_without_filter,on_focus=cancelErrorText2,on_change=cancelErrorText2,border_width=5,border_color=ft.colors.BLUE_300,bgcolor=ft.colors.BLACK,color=ft.colors.WHITE,keyboard_type=ft.KeyboardType.NAME,selection_color=ft.colors.BLUE_300,on_blur=dismiss_txt)

    search_button=ft.IconButton(icon=ft.icons.SEARCH, tooltip='Search', on_click=search_text2.on_submit)
    if switch_language.value=='Arabic':
        search_button.tooltip='ابحث'
    search_text2.suffix=ft.Row([
        search_button,filter_button
    ],width=85)
    info_text=ft.Text("INFO")
    if switch_language.value=='Arabic':
        info_text.value='حول'
    pb = ft.PopupMenuButton(icon=ft.icons.MENU,
                            items=[
                                ft.PopupMenuItem(content=r2,
                                                 on_click=search
                                                 ),
                                ft.PopupMenuItem(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.icons.INFO),
                                            info_text,
                                        ]
                                    ),

                                    on_click=open_dlg
                                ),
                            ]
                            )


    def CancelSearching(e):
        AB.title=txt2
        AB.leading =pb
        search_text2.value=''
        page.update()
    txt1= search_text2



    txt2=ft.Text("Home", size=30,visible=True,weight=ft.FontWeight.W_900)
    if switch_language.value=='Arabic':
        txt2.value='الصفحة الرئيسية'
    AB=ft.AppBar(
        title=txt2,
        bgcolor=ft.colors.GREEN_900
        ,toolbar_height=100)
    collage_sign=ft.Image(src=f"/sign.jpeg",width=50,height=50,border_radius=30)
    def Home(e):
        page.splash = ft.ProgressBar(visible=True)
        page.update()
        time.sleep(7)
        page.splash = ft.ProgressBar(visible=False)
        page.go("/Home")
    def route_change(e):

        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [
                        ft.AppBar(
                            title=ft.Text("Welcome", size=30, weight=ft.FontWeight.W_900),
                            bgcolor=ft.colors.GREEN_900

                        ),
                        ft.Column([
                            ft.Image(
                                src=f"/cover.png",
                                fit=ft.ImageFit.COVER,

                            )], scroll='always', expand=True,
                        ),
                        switch_language
                        ,
                        ft.FloatingActionButton(
                            content=ft.Text(value=("Get Started"), text_align="LEFT"),
                            bgcolor=ft.colors.GREEN_900,
                            shape=ft.RoundedRectangleBorder(radius=5),
                            width=100,
                            mini=True,
                            on_click=Home
                        ),

                ]
                )

            )

        AB.leading =pb
        AB.actions=[
            collage_sign,
            toggledarklight

        ]




        if page.route=='/Home':

            r = ft.Row(wrap=True, scroll='always', expand=True, width=2000)
            if switch_language.value=='english':
                symptoms_list = list(symptoms_set['dignosis'])
            else:
                symptoms_list = list(symptoms_set['الاعراض'])
            options = []
            options2 = []
            None_option = ft.dropdown.Option("None")
            None_option.disabled = True
            options.append(None_option)
            options2.append(None_option)
            governorates_list.sort(reverse=False)
            Specialties_list.sort(reverse=False)
            for governorates in governorates_list:
                region = re.sub(r'[0-9]', '', governorates)
                region = region.strip('()')
                region = region.strip(' ')
                if switch_language.value=='Arabic':
                    options.append(ft.dropdown.Option(text=region, key=governorates))
                else:
                    region=translator.translate(region,dest='en')
                    options.append(ft.dropdown.Option(text=region.text, key=governorates))
            for Specialty in Specialties_list:
                if switch_language.value=='Arabic':
                    options2.append(ft.dropdown.Option(Specialty))
                else:
                    Specialty=translator.translate(Specialty,dest='en')
                    options2.append(ft.dropdown.Option(text=Specialty.text,key=Specialty.origin))
            dropdown2.options=[]
            dropdown.options=[]
            dropdown2.options = options2
            dropdown.options = options
            for i in symptoms_list:
                symptoms_text = ft.Text(value=i, weight=ft.FontWeight.W_900)

                todo_check = ft.Checkbox(fill_color=ft.colors.GREEN_900, value=False, check_color=ft.colors.GREEN,
                                         on_focus=cancelErrorText2)
                r.controls.append(
                    ft.Container(
                        ft.Row([todo_check, symptoms_text]),
                        width=270,
                        height=100,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.GREEN,
                        border=ft.border.all(1, ft.colors.BLACK),
                        border_radius=ft.border_radius.all(10),

                    )
                )
                check_boxes_list.append(todo_check)
            symptoms_text2=ft.Text("Please Enter your symptoms : ", size=50, weight=ft.FontWeight.W_900,
                                text_align='LEFT')
            if switch_language.value=='Arabic':
                pb.tooltip='القائمة'
                symptoms_text2.value='برجاء اختيار الاعراض '
                submit_text.value = 'ارسال'
                reset_text.value = 'اعادة ضبط'
                wait_massage.value = 'برجاء الانتظار'
                description_text.value = 'ان ذلك الموقع مشروع تخرج خاص بكلية حاسبات ومعلومات جامعة عين شمس يشخص الحالات المرضية عن طريق الاعراض'
                create_text.value = 'أنشأ بواسطة :'
                name1.value = 'عبدالرحمن علي احمد'
                name2.value = 'احمد امام محمد'
                name3.value = 'عمر خالد السيد'
                name4.value = 'محمود احمد جابر'
                name5.value = 'احمد محمد حسين'
                supervision_text.value = 'تحت اشراف :'
                doctor_name.value = 'د/دينا الصياد'
                doctor_title.value = 'محاضر في كلية حاسبات ومعلومات جامعة عين شمس،قسم حسابات علمية'
                TA_name.value = 'د/رزق محمد'
                TA_Title.value = 'مدرس مساعد في كلية حاسبات ومعلومات جامعة عين شمس '
                txt2.value = 'الصفحة الرئيسية'
                info_text.value='حول'
                search_txt.value='بحث'
                search_text.label = 'اسم الطبيب'
                advanced_search_text.value = 'البحث المتقدم'
                advanced_search_icon.tooltip = 'بحث'
                filter_button.tooltip='البحث المتقدم'
                search_button.tooltip='بحث'
                dropdown.label='المحافظة'
                dropdown.hint_text='اختر محافظتك'
                dropdown2.label='التخصص'
                dropdown2.hint_text='اختر التخصص'
            else:
                pb.tooltip='menu'
                symptoms_text2.value = 'Please Enter your symptoms :'
                submit_text.value = 'Submit'
                reset_text.value = 'Reset'
                wait_massage.value = 'Please Wait..'
                description_text.value = 'This is a graduation project for the faculty of computer and information science-Ain shams university that diagnoses disease cases by symptoms.'
                create_text.value = 'Created by :'
                name1.value = 'Abdelrahman Ali Ahmed'
                name2.value = 'Ahmed Emam Mohamed'
                name3.value = 'Omar Khaled Elsayed'
                name4.value = 'Mahmoud Ahmed Gaber'
                name5.value = 'Ahmed Mohamed Hussien'
                supervision_text.value = 'Under Supervision of'
                doctor_name.value = 'Dr. Dina Elsayad'
                doctor_title.value = '(lecturer at Faculty of Computer and Information Science, Scientific Computing Department )'
                TA_name.value = 'TA. Rezq Muhammed'
                TA_Title.value = '(Teaching Assistant at Faculty of Computer and Information Science, Ain Shams University)'
                txt2.value = 'Home'
                info_text.value='INFO'
                search_txt.value='search'
                search_text.label = "Doctor's Name"
                advanced_search_text.value = 'advanced search'
                advanced_search_icon.tooltip = 'search'
                filter_button.tooltip='advanced search'
                search_button.tooltip='بحث'
                dropdown.label='Governorate'
                dropdown.hint_text='Select governorate'
                dropdown2.label='Specialty'
                dropdown2.hint_text='Select Specialty'
            page.views.append(
                flet.View(
                    "/Home",
                    [

                        AB,
                        symptoms_text2,

                        r,
                        ft.Row([page.floating_action_button,
                                page.floating_reset_button]),

                    ],
                )
            )
            page.overlay.append(dlg2)
            page.overlay.append(dlg)
        massage1 = ft.Text(value='No Data found', weight=ft.FontWeight.BOLD,size=100)
        massage2 = ft.Text(value='Found Results', weight=ft.FontWeight.BOLD,size=20)
        if switch_language.value=='Arabic':
            massage1.value='لا توجد نتائج'
            massage2.value='النتائج المتاحة'
        c = ft.Container()
        search_results_text = ft.Text("Search Results", size=30, weight=ft.FontWeight.W_900)
        if page.route=="/search":
            r3 = ft.Row(wrap=True, scroll='always', expand=True, width=2000, height=1000)
            if search_results_list == [[]]:
                dlg2.open=False
                c.content=ft.Row([massage1],alignment=ft.MainAxisAlignment.CENTER)
                page.update()
            else:
                 c.content=massage2
                 for i in search_results_list:
                    for j in i:
                            phone=str(j[6]).replace('\n',',')
                            phone = phone.replace('/', ',')
                            phone = phone.replace('-', ',')
                            phone = phone.replace('_', ',')
                            region=re.sub(r'[0-9]','',j[0])
                            region=region.strip('()')
                            region=region.strip(' ')
                            details=ft.Column([
                                        ft.Icon(ft.icons.MEDICAL_INFORMATION, size=80),
                                        ft.Row([ft.Icon(ft.icons.PERSON,tooltip='Name',size=28), ft.Text(value=j[4],weight=ft.FontWeight.BOLD,size=28)]),
                                        ft.Row([ft.Icon(ft.icons.LOCATION_CITY,tooltip='governorate',size=28),ft.Text(value=region,weight=ft.FontWeight.BOLD,size=28)]),
                                        ft.Row([ft.Icon(ft.icons.LOCATION_CITY,tooltip='region',size=28), ft.Text(value=str(j[1]),weight=ft.FontWeight.BOLD,size=28)]),
                                        ft.Row([ft.Icon(ft.icons.GPS_FIXED, tooltip='address', size=28),  ft.Text(value=str(j[5]),weight=ft.FontWeight.BOLD,size=28)]),
                                        ft.Row([ft.Icon(ft.icons.PHONE, tooltip='phone number(s)', size=28), ft.Text(value=phone, weight=ft.FontWeight.BOLD, size=28)]),
                                        ft.Row([ft.Icon(ft.icons.WORK, tooltip='specialization', size=28), ft.Text(value=str(j[3]), weight=ft.FontWeight.BOLD, size=28)]),


                                    ],alignment=ft.MainAxisAlignment.CENTER)

                            r3.controls.append(
                                    ft.Container(
                                        details,
                                        width=1020,
                                        height=440,

                                        bgcolor=ft.colors.GREEN,
                                        border=ft.border.all(1, ft.colors.BLACK),
                                        border_radius=ft.border_radius.all(10),
                                        padding=ft.padding.only(left=10)
                                    )
                            )

            if switch_language.value=='Arabic':
                search_results_text.value='نتائج البحث'
            page.views.append(
                flet.View(
                    "/search",
                    [
                        ft.AppBar(
                            title=search_results_text,
                            bgcolor=ft.colors.GREEN_900,
                            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=view_pop, tooltip='Back'),
                            actions=[
                                collage_sign,
                                toggledarklight

                            ]
                        )
                        ,c
                        ,r3





                    ],

                )
            )

        if page.route == "/Advanced-search":
                dlg2.open = False
                dlg2.update()
                r4 = ft.Row(wrap=True, scroll='always', expand=True, width=2000, height=1000)
                if search_results_list2 == [[]] and dropdown2.value != None and dropdown.value != None:
                    c.content = ft.Row([massage1], alignment=ft.MainAxisAlignment.CENTER)
                    page.update()
                else:
                    c.content=massage2
                    for i in range(len(search_results_list2)):
                        for j in range(len(search_results_list2[i])):
                            phone = str(search_results_list2[i][j][6]).replace('\n', ',')
                            phone = phone.replace(' ', ',')
                            phone = phone.replace('/', '')
                            phone = phone.replace('-', '')
                            phone = phone.replace('_', ',')
                            region = re.sub(r'[0-9]', '', search_results_list2[i][j][0])
                            region = region.strip('()')
                            region = region.strip(' ')
                            details2 = ft.Column([
                                ft.Icon(ft.icons.MEDICAL_INFORMATION, size=80),
                                ft.Row([ft.Icon(ft.icons.PERSON, tooltip='Name', size=28),
                                        ft.Text(value=search_results_list2[i][j][4], weight=ft.FontWeight.BOLD,
                                                size=28)]),
                                ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='governorate', size=28),
                                        ft.Text(value=region, weight=ft.FontWeight.BOLD, size=28)]),
                                ft.Row([ft.Icon(ft.icons.LOCATION_CITY, tooltip='region', size=28),
                                        ft.Text(value=str(search_results_list2[i][j][1]), weight=ft.FontWeight.BOLD,
                                                size=28)]),
                                ft.Row([ft.Icon(ft.icons.GPS_FIXED, tooltip='address', size=28),
                                        ft.Text(value=str(search_results_list2[i][j][5]), weight=ft.FontWeight.BOLD,
                                                size=28)]),
                                ft.Row([ft.Icon(ft.icons.PHONE, tooltip='phone number(s)', size=28),
                                        ft.Text(value=phone, weight=ft.FontWeight.BOLD, size=28)]),
                                ft.Row([ft.Icon(ft.icons.WORK, tooltip='specialization', size=28),
                                        ft.Text(value=str(search_results_list2[i][j][3]), weight=ft.FontWeight.BOLD,
                                                size=28)]),
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            r4.controls.append(
                                    ft.Container(
                                        details2,
                                        width=1020,
                                        height=440,
                                        alignment=ft.alignment.center,
                                        bgcolor=ft.colors.GREEN,
                                        border=ft.border.all(1, ft.colors.BLACK),
                                        border_radius=ft.border_radius.all(10),
                                        padding=ft.padding.only(left=10)
                                    )
                                )
                page.views.append(
                    flet.View(
                        "/Advanced-search",
                        [
                            ft.AppBar(
                                title=search_results_text,
                                bgcolor=ft.colors.GREEN_900,
                                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=view_pop, tooltip='Back'),
                                actions=[
                                    collage_sign,
                                    toggledarklight

                                ]
                            )
                            , c
                            , r4


                        ],

                    )
                )
                dlg2.open=False
                page.update()

    def view_pop(e):
        page.views.clear()
        search_results_list.clear()
        search_text2.value=None
        search_text2.error_text=None
        AB.title = txt2
        check_boxes_list.clear()
        AB.leading = pb
        page.go('/Home')
        search_text.error_text=None
        page.update()
    def view_pop2(e):
        page.views.clear()
        page.go('/')
        page.update()
        search_text2.value = None
        search_text2.error_text = None
        AB.title = txt2
        check_boxes_list.clear()
        AB.leading = pb
        search_text.error_text = None
        search_results_list2.clear()
        search_results_list.clear()
        page.update()

    encoder = LabelEncoder()
    encoder.fit_transform(train_set["prognosis"])
    encoder.transform(test_set["prognosis"])
    filename1 = 'assets/SVM.h5'
    Model = pickle.load(open(filename1, 'rb'))
    page.on_route_change = route_change
    page.go(page.route)






flet.app(target=main,assets_dir="assets")