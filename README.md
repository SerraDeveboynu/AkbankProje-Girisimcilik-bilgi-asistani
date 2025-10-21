# AkbankProje-Girisimcilik-bilgi-asistani
  TÜBİTAK, KOSGEB ve TEKNOFEST verilerini kullanarak öğrenci girişimcilere hibe ve destekler hakkında bilgi veren, RAG tabanlı bir chatbot projesidir.

## 🚀 Projenin Amacı

  Bu projenin temel amacı, 'TÜBİTAK, KOSGEB ve TEKNOFEST' gibi önemli ulusal kaynaklardan edinilen bilgilerle donatılmış bir "Girişimcilik Bilgi Asistanı" oluşturmaktır.

-  Geliştirilen bu RAG tabanlı chatbot, özellikle üniversite öğrencileri ve genç girişimcilerin, hibe programları, başvuru süreçleri, yarışmalar ve diğer destekler hakkında hızlı ve doğru bilgilere ulaşmasını sağlamayı hedeflemektedir.
-  Bu sayede, karmaşık ve dağınık bilgilerin tek bir arayüzde toplanması ve kullanıcıların sorularına anında yanıt verilmesi amaçlanmıştır.

---

## 📊 Veri Seti Hakkında Bilgi

Projede kullanılan veri seti, üç ana kaynaktan (TÜBİTAK, KOSGEB ve TEKNOFEST resmi web siteleri) manuel olarak toplanmıştır.
-  Veri toplama aşamasında, her bir kurumun hibe, destek ve başvuru süreçleri ile ilgili 2-3 sayfalık metinler kopyalanarak ayrı `.txt` dosyaları haline getirilmiştir.
-  Bu süreçte herhangi bir programatik veri kazıma (web scraping) yöntemi kullanılmamış, içerikler doğrudan ilgili sayfalardan kopyalanıp yapıştırılmıştır. Toplanan bu metinler, projenin temel bilgi havuzunu oluşturmaktadır.

---

## 🛠️ Kullanılan Yöntemler ve Çözüm Mimarisi

  Bu chatbot projesi, veriye dayalı doğru cevap üretimi için "RAG (Retrieval Augmented Generation)" mimarisi temel alınarak geliştirilmiştir.

### "RAG Mimarisi Adımları"

1. Metin Parçalama ve Vektörleştirme: Toplanan `.txt` dosyaları parçalara ayrılır ve açık kaynaklı bir 'Embedding Modeli' kullanılarak sayısal vektörlere dönüştürülür.
2. Depolama: Vektörler, hızlı arama için 'ChromaDB' Vektör Veritabanı'nda depolanır.
3. Sorgulama: Kullanıcıdan gelen soru vektörleştirilir ve ChromaDB'de en benzer metin parçalarını bulmak için kullanılır.
4. Cevap Üretme: En alakalı metin parçaları, bağlam (context) olarak 'Google'ın Gemini API'si' (Generation Model) tarafından kullanılır ve nihai, bilgilendirici cevap oluşturulur.

### "Kullanılan Teknolojiler"

-  RAG Pipeline Framework: LangChain
-  Generation Model (LLM): Google Gemini API
-  Embedding Model: Açık kaynaklı bir embedding modeli (örneğin: `sentence-transformers` ailesinden)
-  Vektör Veritabanı: ChromaDB

---

## ✅ Elde Edilen Sonuçlar

Geliştirilen "Girişimcilik Bilgi Asistanı" projesi, belirtilen kurumların destek programları hakkında doğru ve hızlı yanıtlar verebilme yeteneği göstermiştir.
-  Yapılan testlerde, kullanıcıların hibe şartları, başvuru tarihleri ve süreçleri gibi konulardaki sorularına, toplanan veriler ışığında tutarlı ve bilgilendirici cevaplar sunulmuştur.
-  Proje, web arayüzü sayesinde son kullanıcıya kolayca ulaşılabilir hale getirilmiş ve girişimcilik ekosistemine katkı sağlayacak bir bilgi kaynağı olarak tasarlanmıştır.

---

## 🌐 Web Arayüzü (Deploy Linki)

-  Projenin çalışan web arayüzüne aşağıdaki linkten ulaşabilirsiniz.

    Web Arayüzü Linki: `https://akbankproje-girisimcilik-bilgi-asistani-hupx3ffynvcx64z5d7bmzw.streamlit.app/`
