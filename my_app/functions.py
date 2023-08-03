import pandas as pd
from my_app import db
from my_app.models import Users, Poems, Speechs, Stories, Beyts


def add_some():
    if Users.query.count() < 1:
        admin = Users(username="admin",
                      phone_email="admin@gmail.com",
                      password="very_secret",
                      name="شاه بیت")
        db.session.add(admin)
        db.session.commit()

        i_speech = Speechs(grade='g', user_id=1,
                           speech='اگر بر دشمنت دست یافتی بخشیدن او را شکرانه پیروزی ات قرار بده',
                           wise="امیرالمومنین")
        db.session.add(i_speech)
        db.session.commit()

        i_poem = Poems(grade='g',
                       user_id=1,
                       beyt1_1='هوا هوای بهار است و باده باده ناب',
                       beyt1_2='به خنده خنده بنوشیم جرعه جرعه شراب',
                       beyt2_1='در این پیاله ندانم چه ریختی پیداست',
                       beyt2_2='که خوش به جان هم افتاده اند آتش و آب',
                       beyt3_1='مگر نه خاک در این خرابه باید شد',
                       beyt3_2='بیا که کام بگیریم از این جهان خراب',
                       poet='فریدون مشیری')
        db.session.add(i_poem)
        db.session.commit()

        i_story = Stories(grade='g', user_id=1, writer='ناشناس',
                          title='یک با یک برابر نیست',
                          story="""معلم پای تخته داد میزد.
                          صورتش از خشم گلگون بود
                          و دستانش به زیر پوششی از گرد پنهان بود
                          ولی آخر کلاسی ها لواشک بین خود تقسیم میکردند
                          و آن یک گوشه دیگر جوانان را ورق میزد.
                          برای آنکه بیخود های و هو میکرد.
                          و با آن شور بی پایان
                          تساوی های جبری را نشان میداد
                          به روی تخته ای کز ظلمتی تاریک
                          غمگین بود
                          تساوی را چنین بنوشت:
                          یک با یک برابر هست.
                          از میان جمع شاگردان یکی برخواست
                          (همیشه یک نفر باید به پا خیزد)
                          به آرامی سخن سر داد:
                          تساوی اشتباهی فاحش و محض است,
                          نگاه بچه ها ناگه به یک سو خیره گشت
                          معلم مات برجا ماند
                          و او پرسید:
                          اگر یک فرد انسان واحد یک بود,
                          آیا باز یک با یک برابر بود؟
                          سکوت مدهشی بود و سوالی سخت.
                          معلم خشمگین فریاد زد:
                          آری برابر بود!
                          و او با پوزخندی گفت:
                          اگر یک فرد انسان واحد یک بود,
                          آنکه زور و زر به دامن داشت
                          بالا بود؟
                          و آنکه قلبی پاک و دستی فاقد زر داشت
                          پایین بود؟
                          اگر یک فرد انسان واحد یک بود
                          آن که صورت نقره گون چون قرص مه میداشت,
                          بالا بود؟
                          وان سیه چرده که مینالید,
                          پایین بود؟
                          اگر یک فرد انسان واحد یک بود,
                          این تساوی زیر و رو میشد.
                          حال میپرسم یک اگر با یک برابر بود
                          نان و مال مفت خور از کجا آماده میگردید؟
                          یا چه کس دیوار چین ها را بنا میکرد؟
                          یک اگر با یک برابر بود,
                          پس که زیر پشت بار فقر خم میشد؟
                          یا که زیر ضربت شلاق له میگشت؟
                          یک اگر با یک برابر بود,
                          پس چه کس آزادگان را در قفس میکرد؟
                          پس معلم ناله آسا گفت:
                          بچه ها در جزوه های خویش بنویسید:
                          «یک با یک برابر نیست»
                          """)
        db.session.add(i_story)
        db.session.commit()

        ds = pd.read_csv("Data.csv")
        for i in range(len(ds) - 1):
            beyt_aval = str(ds.poem1[i])
            bet_dovom = str(ds.poem2[i])
            shyer = str(ds.poet[i])
            start = int(ds.start[i])
            end = int(ds.stop[i])
            i_beyt = Beyts(grade='g', user_id=1,
                           mesra1=beyt_aval,
                           mesra2=bet_dovom,
                           poet=shyer,
                           opening=start,
                           ending=end)
            db.session.add(i_beyt)
            db.session.commit()