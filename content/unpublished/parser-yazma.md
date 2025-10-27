#Python ile 50 Satirda Hesap Makinesi Yapmak

Bu yazida bir aritmetik gosterimin nasil ayristirilip incelenebilecegini, genel olarak bir ayristiricinin nasil calisabilecegini anlatacagim. Isimiz bittiginde 1+2*-(-3+2)/5.6+3 gibi bir matematik islemini sonuclandirabilen bir makineye sahip olacagiz.

Amacim diller hakkinda, basit ve eglenceli bir ders verebilmek.

#Gramerler

Ayristirmanin ve formal gramerlerin nasil calistigini bilmeyenler icin kucuk bir giris yapalim. Bir formal grammer bir metnin nasil ayristirilacagina dair hirearsik bir kurallar listesidir. Her kural giris metninin bir kismi ile eslesir.

Asagida 1+2+3+4 girisini islemek icin kullanilabilecek bir kural kumesi var:

    Kural #1 - ekle, _ekle+sayi_ VEYA _sayi+sayi_ ifadelerinden olusur.

 Bu kurali EBNF seklinde ifade etmek istedigimizde:

    ekleme: ekleme '+' sayi | sayi '+' sayi;

Ayristiricimiz her geciste _ekleme+sayi_ veya _sayi+sayi_ desenine uyan bir bolum arayacak, bulabildiginde ise onu bir ekleme islemine donusturecek.

Simdi adim adim tek kuralli ayristiricimizi calistiralim:

Adim 1:

Girisimiz 1+2+3+4, seklinde bir metindi, ayristiricimiz ilk geciste bu metini [sayi(1), aritmetik('+') sayi+sayi+sayi olarak isaretler.

Adim 2:

Kural #1'deki _ekle+sayi_ deseni su anda hic bir yerde gozukmese de _sayi+sayi_ desenini girisin basinda var. Ayristiricimiz bastaki _sayi+sayi_ desenini ekleme desenine donusturur.

Adim 3:

Bu geciste giris, ekleme + sayi + sayi, ekleme kuralimizdaki ekleme+sayi
