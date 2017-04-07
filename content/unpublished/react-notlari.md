React Notları:

React Facebook tarafından ortalara atılmış bir javascript kütüphanesi. MVC
desenli tasarımlarda V (View) katmanını oluşturduğu söylense de redux gibi
kütüphanelerle birleştiğinde başlı başına bir çalışma tasarım şemasına sahip
olduğunuz söyleniyor. Bu yazıda sıfırdan başlayarak react native ile bir
uygulama geliştirmeye çalışacağız.

Ben kendi telefonum Android olduğu için Android üzerinden ilerleyeceğim.

Getirileri:

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

Avantajları:

React web sayfalarını render ederken gerçek DOM'u değil de kendi salan DOM'unu
kullanıyor ve burada güncellemeleri değişiklikleri yaptıktan sonra gerçek DOM'a
bu değişiklikleri aktarıyor. Bu da muazzam bir performans artışı demek.

React sunucu ve istemci tarafında kullanılabiliyor. React ile hazırladığınız
componentler sonradan render edilmek zorunda değil.

Component ve veri tipleri javascript kodunun okunabilirliğini arttırıyor.

Sınırlamaları:

React sadece view katmanını temsil ettiği için geliştirme ortamınızı tamamlamak
adına başka kütüphanelere ihtiyaç duyabiliyorsunuz.

React'ın kullandığı JSX markup dili bazı geliştiricilere acayip gözükebiliyor.

ADIM 1 - GLOBAL GEREKLİ PAKETLERİN KURULMASI:

Öncelikle babel pakedini kurmanız gerekiyor. Bu paket javascript yazarken
ES2015 standardını kullanabilmenizi sağlıyor. ES2015 standardı ile yazdığınız
javascript kodunun eğer broser desteklemiyor ise downgrade edilmiş bir
versionunu compile ediyor. Artık modern javascript yazmak için babel kullanmak
zorunlu gibi bir şey.

$ npm install -g babel babel-cli


