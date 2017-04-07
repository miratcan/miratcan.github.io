#Python ile 50 Satırda Hesap Makinesi Yapmak

Bu yazıda bir aritmetik gösterimin nasıl ayrıştırılıp incelenebileceğini, genel olarak bir ayrıştırıcının nasıl çalışabileceğini anlatacağım. İşimiz bittiğinde 1+2*-(-3+2)/5.6+3 gibi bir matematik işlemini sonuçlandırabilen bir makineye sahip olacağız.

Amacım diller hakkında, basit ve eğlenceli bir ders verebilmek.

#Gramerler

Ayrıştırmanın ve formal gramerlerin nasıl çalıştığını bilmeyenler için küçük bir giriş yapalım. Bir formal grammer bir metnin nasıl ayrıştırılacağına dair hirearşik bir kurallar listesidir. Her kural giriş metninin bir kısmı ile eşleşir.

Aşağıda 1+2+3+4 girişini işlemek için kullanılabilecek bir kural kümesi var:

    Kural #1 - ekle, _ekle+sayı_ VEYA _sayı+sayı_ ifadelerinden oluşur.

 Bu kuralı EBNF şeklinde ifade etmek istediğimizde:

    ekleme: ekleme '+' sayı | sayı '+' sayı;

Ayrıştırıcımız her geçişte _ekleme+sayı_ veya _sayı+sayı_ desenine uyan bir bölüm arayacak, bulabildiğinde ise onu bir ekleme işlemine dönüştürecek.

Şimdi adım adım tek kurallı ayrıştırıcımızı çalıştıralım:

Adım 1:

Girişimiz 1+2+3+4, şeklinde bir metindi, ayrıştırıcımız ilk geçişte bu metini [sayı(1), aritmetik('+') sayı+sayı+sayı olarak işaretler.

Adım 2:

Kural #1'deki _ekle+sayı_ deseni şu anda hiç bir yerde gözükmese de _sayı+sayı_ desenini girişin başında var. Ayrıştırıcımız baştaki _sayı+sayı_ desenini ekleme desenine dönüştürür.

Adım 3:

Bu geçişte giriş, ekleme + sayı + sayı, ekleme kuralımızdaki ekleme+sayı
