# Javascript Uzmani Olmayanlar Icin React-Native Anlatimi

React Facebook tarafindan ortalara atilmis bir javascript kutuphanesi. MVC
desenli tasarimlarda V (View) katmanini olusturdugu soylense de redux gibi
kutuphanelerle birlestiginde basli basina bir calisma tasarim semasina sahip
oldugunuz soyleniyor. Bu yazida sifirdan baslayarak react native ile bir
uygulama gelistirmeye calisacagiz.

> Okumadan Once:
>
>Hedef isletim sistemim Android, gelistirme yaptigim isletim sistemi ise OSX
>olacak. Bu yuzden ornegin IOS icin gelistirme yapmak istiyorsaniz bu yazi
>bir yere kadar yeterli olacaktir.
>
>Gelistirme yaptiginiz sistemde NodeJS, NPM ve Homebrew kurulu olmalidir.

## Getirileri:

1) JSX adinda bir markup dili getiriyor, bunu kullanmak zorunlu olmasa da
siddetle tavsiye edilmekte. Ha HTML yerine kullanilmasi avantajli mi?
Tartisilir.

2) Components - React bir web sayfasi ya da uygulamayi tasarlarken HTML
etiketleri olarak degil de gorunum bilesenleri tasarlamanizi sagliyor. Ne
faydasi var diyecek olursaniz, bilesenler bir kere duzgun tasarlandiktan sonra
farkli projelerde kullanilabiliyorlar. Ornegin hesap makinesi adinda buyuk bir
bilesen yaparsaniz bunu yaptiginiz farkli farkli uygulamalara takabiliyorsunuz.

3) Cift Tarafli Veri Akisi: React componentlerin veriden yola cikarak
gosterimini, ayni zamanda da verinin componentlerin durumuyla guncellenmesini
saglayabiliyor. Bunu flux adinda bir kutuphane ile yapiyor.

## Avantajlari:

React web sayfalarini render ederken gercek DOM'u degil de kendi salan DOM'unu
kullaniyor ve burada guncellemeleri degisiklikleri yaptiktan sonra gercek DOM'a
bu degisiklikleri aktariyor. Bu da muazzam bir performans artisi demek.

React sunucu ve istemci tarafinda kullanilabiliyor. React ile hazirladiginiz
componentler sonradan render edilmek zorunda degil.

Component ve veri tipleri javascript kodunun okunabilirligini arttiriyor.

## Sinirlamalari:

React sadece view katmanini temsil ettigi icin gelistirme ortaminizi tamamlamak
adina baska kutuphanelere ihtiyac duyabiliyorsunuz.

React'in kullandigi JSX markup dili bazi gelistiricilere acayip gozukebiliyor.

### ADIM 1 - GLOBAL GEREKLI PAKETLERIN KURULMASI:

Oncelikle babel pakedini kurmaniz gerekiyor. Bu paket javascript yazarken
ES2015 standardini kullanabilmenizi sagliyor. ES2015 standardi ile yazdiginiz
javascript kodunun eger broser desteklemiyor ise downgrade edilmis bir
versionunu compile ediyor. Artik modern javascript yazmak icin babel kullanmak
zorunlu gibi bir sey.

$ npm install -g babel babel-cli react-native-cli

### ADIM 2 - ANDROID SDK'NIN KURULUMU:

Yazacaginiz uygulamalarin telefonda ya da bir telefon emulatorunde
calistirilmasi gerekiyor. Eger yazdigimiz kodlarin sonucunu sanal ya da degil
bir Android makine uzerinde gormek istiyorsaniz (benim senaryomda istiyoruz)
Android SDK'nin kurulumunu yapmamiz gerekiyor.

    $ brew install android-sdk

Brew guzel alet, Android SDK'nin ciplak haliyle kurulumunu yaptik. Ardindan
yapmamiz gereken sey ise ANDROID_HOME ortam degerinin set edilmesi. Bu deger
Android SDK'yi kurdugunuz yer olmali.

Mac sisteminizde asagidaki satiri (eger yoksa) ~/.bashrc, ~/.bash_profiel ya
da fish kullaniyorsaniz adini hatirlamadigim baska bir dosya icine yazmaniz
gerekiyor:

    export ANDROID_HOME=/usr/local/opt/android-sdk

Burada tekrar hatirlatmamda fayda var verdigimiz yolun SDK'nin kurulu oldugu
yeri gostermesi gerekiyor. Kontrol edip yolu ona gore gerekiyorsa degistirin.

Bu degiskeni dogru olarak degistirdiyseniz asagidaki komutun ciktisi sunun
gibi olmalidir:

    ls $ANDROID_HOME
    INSTALL_RECEIPT.json add-ons              build-tools
    extras               platforms            sources
    temp                 README               bin
    etc                  platform-tools       samples
    system-images        tools

Bu asamadan sonra SDK icin cesitli paketleri yuklememiz gerekiyor.

    $ android

Bu komuttan sonra acilacak Android SDK Manager uzerinden su listeledigim
paketleri kurun:

 * Android SDK Build-tools versiyon 23.0.1
 * Android 6.0 (API 23)
 * Local Maven repository for Support Libraries (Extras bolumunde cikiyor)


![](https://facebook.github.io/react-native/releases/0.23/img/AndroidSDK1.png)
![](https://facebook.github.io/react-native/releases/0.23/img/AndroidSDK2.png)


### ADIM 3 - REACT NATIVE ILE PROJENIN BASLATILMASI

Yukaridaki kurulumu yaptiktan sonra artik react-native komutu bizim icin
calistirilabilir olmali. Projeyi olusturabiliriz:

    $ react-native init ReactCalculator

Bu komut baya bir indirme yapiyor  ve benim gibi Python gelistiricilerine
oldukca devasa gozukecek bir proje agaci yaratiyor.

    $ cd ReactCalculator
    $ ReactCalculator/ $ ls
    __tests__        app.json         index.ios.js     node_modules
    android          index.android.js ios              package.json

Umuyorum bura olusturulan js dosyalari compile etme asamasinda eleniyor,
gereksiz olanlar calistirilabilir pakede dahil olmuyordur.

Bu noktada bilmemiz gereken bazi seyler sunlar:

  * React Native paket yoneticisi olarak NPM kullaniyor. Dolayisiyla
    node_modules dizini kurdugumuz, kuracagimiz paketleri barindiriyor.

  * "android" ve "ios" dizinleri android ve ios projeleri icin uretilmis kodu
    barindiriyor. Android Studio ya da XCode kullanarak acip, incelenebilir.

  * index.android.js ve index.ios.jsedosyalari bizim kaynak kodumuzun giris
    noktalari oluyor.

### ADIM 3 - PROJENIN BASLATILMASI

Projeyi baslatmak icin oncelikle Android SDK'nin kurulu olmasi gerekmekte.

Kaynaklar:

 * https://www.tutorialspoint.com/react_native/
 * https://facebook.github.io/react-native/releases/0.23/docs/android-setup.html
 * https://kylewbanks.com/blog/react-native-tutorial-part-1-hello-react

