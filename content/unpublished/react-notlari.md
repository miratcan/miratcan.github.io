# Javascript Uzmanı Olmayanlar İçin React-Native Anlatımı

React Facebook tarafından ortalara atılmış bir javascript kütüphanesi. MVC
desenli tasarımlarda V (View) katmanını oluşturduğu söylense de redux gibi
kütüphanelerle birleştiğinde başlı başına bir çalışma tasarım şemasına sahip
olduğunuz söyleniyor. Bu yazıda sıfırdan başlayarak react native ile bir
uygulama geliştirmeye çalışacağız.

> Okumadan Önce:
>
>Hedef işletim sistemim Android, geliştirme yaptığım işletim sistemi ise OSX
>olacak. Bu yüzden örneğin IOS için geliştirme yapmak istiyorsanız bu yazı
>bir yere kadar yeterli olacaktır.
>
>Geliştirme yaptığınız sistemde NodeJS, NPM ve Homebrew kurulu olmalıdır.

## Getirileri:

1) JSX adında bir markup dili getiriyor, bunu kullanmak zorunlu olmasa da
şiddetle tavsiye edilmekte. Ha HTML yerine kullanılması avantajlı mı?
Tartışılır.

2) Components - React bir web sayfası ya da uygulamayı tasarlarken HTML
etiketleri olarak değil de görünüm bileşenleri tasarlamanızı sağlıyor. Ne
faydası var diyecek olursanız, bileşenler bir kere düzgün tasarlandıktan sonra
farklı projelerde kullanılabiliyorlar. Örneğin hesap makinesi adında büyük bir
bileşen yaparsanız bunu yaptığınız farklı farklı uygulamalara takabiliyorsunuz.

3) Çift Taraflı Veri Akışı: React componentlerin veriden yola çıkarak
gösterimini, aynı zamanda da verinin componentlerin durumuyla güncellenmesini
sağlayabiliyor. Bunu flux adında bir kütüphane ile yapıyor.

## Avantajları:

React web sayfalarını render ederken gerçek DOM'u değil de kendi salan DOM'unu
kullanıyor ve burada güncellemeleri değişiklikleri yaptıktan sonra gerçek DOM'a
bu değişiklikleri aktarıyor. Bu da muazzam bir performans artışı demek.

React sunucu ve istemci tarafında kullanılabiliyor. React ile hazırladığınız
componentler sonradan render edilmek zorunda değil.

Component ve veri tipleri javascript kodunun okunabilirliğini arttırıyor.

## Sınırlamaları:

React sadece view katmanını temsil ettiği için geliştirme ortamınızı tamamlamak
adına başka kütüphanelere ihtiyaç duyabiliyorsunuz.

React'ın kullandığı JSX markup dili bazı geliştiricilere acayip gözükebiliyor.

### ADIM 1 - GLOBAL GEREKLİ PAKETLERİN KURULMASI:

Öncelikle babel pakedini kurmanız gerekiyor. Bu paket javascript yazarken
ES2015 standardını kullanabilmenizi sağlıyor. ES2015 standardı ile yazdığınız
javascript kodunun eğer broser desteklemiyor ise downgrade edilmiş bir
versionunu compile ediyor. Artık modern javascript yazmak için babel kullanmak
zorunlu gibi bir şey.

$ npm install -g babel babel-cli react-native-cli

### ADIM 2 - ANDROID SDK'NIN KURULUMU:

Yazacağınız uygulamaların telefonda ya da bir telefon emülatöründe
çalıştırılması gerekiyor. Eğer yazdığımız kodların sonucunu sanal ya da değil
bir Android makine üzerinde görmek istiyorsanız (benim senaryomda istiyoruz)
Android SDK'nın kurulumunu yapmamız gerekiyor.

    $ brew install android-sdk

Brew güzel alet, Android SDK'nın çıplak haliyle kurulumunu yaptık. Ardından
yapmamız gereken şey ise ANDROID_HOME ortam değerinin set edilmesi. Bu değer
Android SDK'yı kurduğunuz yer olmalı.

Mac sisteminizde aşağıdaki satırı (eğer yoksa) ~/.bashrc, ~/.bash_profiel ya
da fish kullanıyorsanız adını hatırlamadığım başka bir dosya içine yazmanız
gerekiyor:

    export ANDROID_HOME=/usr/local/opt/android-sdk

Burada tekrar hatırlatmamda fayda var verdiğimiz yolun SDK'nın kurulu olduğu
yeri göstermesi gerekiyor. Kontrol edip yolu ona göre gerekiyorsa değiştirin.

Bu değişkeni doğru olarak değiştirdiyseniz aşağıdaki komutun çıktısı şunun
gibi olmalıdır:

    ls $ANDROID_HOME
    INSTALL_RECEIPT.json add-ons              build-tools
    extras               platforms            sources
    temp                 README               bin
    etc                  platform-tools       samples
    system-images        tools

Bu aşamadan sonra SDK için çeşitli paketleri yüklememiz gerekiyor.

    $ android

Bu komuttan sonra açılacak Android SDK Manager üzerinden şu listelediğim
paketleri kurun:

 * Android SDK Build-tools versiyon 23.0.1
 * Android 6.0 (API 23)
 * Local Maven repository for Support Libraries (Extras bölümünde çıkıyor)


![](https://facebook.github.io/react-native/releases/0.23/img/AndroidSDK1.png)
![](https://facebook.github.io/react-native/releases/0.23/img/AndroidSDK2.png)


### ADIM 3 - REACT NATIVE ILE PROJENIN BAŞLATILMASI

Yukarıdaki kurulumu yaptıktan sonra artık react-native komutu bizim için
çalıştırılabilir olmalı. Projeyi oluşturabiliriz:

    $ react-native init ReactCalculator

Bu komut baya bir indirme yapıyor  ve benim gibi Python geliştiricilerine
oldukça devasa gözükecek bir proje ağacı yaratıyor.

    $ cd ReactCalculator
    $ ReactCalculator/ $ ls
    __tests__        app.json         index.ios.js     node_modules
    android          index.android.js ios              package.json

Umuyorum bura oluşturulan js dosyaları compile etme aşamasında eleniyor,
gereksiz olanlar çalıştırılabilir pakede dahil olmuyordur.

Bu noktada bilmemiz gereken bazı şeyler şunlar:

  * React Native paket yöneticisi olarak NPM kullanıyor. Dolayısıyla
    node_modules dizini kurduğumuz, kuracağımız paketleri barındırıyor.

  * "android" ve "ios" dizinleri android ve ios projeleri için üretilmiş kodu
    barındırıyor. Android Studio ya da XCode kullanarak açıp, incelenebilir.

  * index.android.js ve index.ios.jsedosyaları bizim kaynak kodumuzun giriş
    noktaları oluyor.

### ADIM 3 - PROJENIN BAŞLATILMASI

Projeyi başlatmak için öncelikle Android SDK'nın kurulu olması gerekmekte.

Kaynaklar:

 * https://www.tutorialspoint.com/react_native/
 * https://facebook.github.io/react-native/releases/0.23/docs/android-setup.html
 * https://kylewbanks.com/blog/react-native-tutorial-part-1-hello-react

