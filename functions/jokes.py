import random

def get_joke():
    jokes = [
        "Sana Erken çalmış fıkrasını anlatayım. Yaramaz Bora, yine sınıfa zil çaldıktan sonra girmişti. Bu durum, öğretmenin canına tak etmiş.\n-Bora! Yine mi geç kaldın? Öf! Bıktım bu yaramaz çocuktan.\n-Ben geç kalmadım ki, öğretmenim. Zil ben gelmeden önce çalmış.",
        "Ödev\nÖğretmeni Kemal´in ödevlerine bakıyormuş.\n-Kemal bu yazı babanın kaleminden çıkmış olmasın?\nKemal:\n-Evet öğretmenim, çünkü yazarken babamın kalemini kullandım.",
        "Çocuk;\n- Nine, senin gözlüklerin herşeyi büyütüyormuş, doğru mu nine?\n- Evet yavrum, Neden sordun?\n- Ne olursun nineciğim, tabağıma tatlı koyarken gözlüğünü çıkar olur mu?",
        "Küçük Ayhan´la Mine konuşuyorlardı:\n-Nehirler nereye dökülür?\n-Denize, tabii.\n-Hepsi mi?\n-Evet.\n-Öyleyse deniz neden taşmıyor?\n-Tabii taşmaz. Denizin dibi sünger dolu. Suyu onlar çekiyor",
        "Harfin Adı\nBirinci sınıf öğretmeni öğrencilerden birine sordu:\n-Bu harfin adı ne?\nÜzülerek karşılık verdi çocuk:\n-Harfi tanıyorum ama, adı bir türlü aklıma gelmiyor...",
        "Konuşmayanlar\nHayat bilgisi dersinde öğretmen sordu:\n- Balıklar neden konuşmaz?\nFunda parmak kadırdı:\n- Öğretmenim, siz de başınızı suya soksanız konuşamazsınız.",
        "Görgü Kuralları\nBabası oğluna görgü kuralarını öğretiyordu :\n'Örneğin oğlum, bir eve gittik. Onları yemek yerken gördük, ilk sözümüz ne olmalı?'\n'Afiyet olsun' der oğlu. Baba;\n'Peki neden bu söylenir?' deyince oğlu ;\n'Neden olacak, buyurun desinler diye.' der.",
        "Saymakla bitmez\nAcıkmış olarak eve dönen Mehmet annesine, 'Akşama ne var?' diye sorunca, annesi;\n'Saymakla bitmez oğlum' dedi. Mehmet;\n'Güzel, nelermiş bunlar?' deyince, annesi gülümseyerek, Pirinç pilavı dedi.",
        "Nasrettin Hoca\nNasrettin Hoca bir gece aniden uyanır.\n– Hatun, çabuk kalk. Gözlüğüm nerede, bulamıyorum?\nKadın, uykulu uykulu,\n– Hoca, gece yarısı niçin gözlük arıyorsun, der.\nHoca telaşlı telaşlı gözlüğünü takar.\n– Ne demek niçin?\nTabii ki rüyada daha iyi görmek için!"
    ]

    random_joke = random.choice(jokes)
    return random_joke