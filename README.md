**Metin2 Farm Botu**<br>

Metin2’de manuel müdahale olmadan verimli bir şekilde farm yapmanıza yardımcı olmak için tasarlanmış otomatik bir araçtır. Python kullanılarak geliştirilmiş olup pyautogui, opencv, keyboard ve pydirectinput gibi çeşitli kütüphanelerden yararlanır. Bu bot; Metin taşlarını bulma gibi oyun içindeki birçok rutin görevi otomatikleştirir.

<img width="1366" height="768" alt="Farmbot" src="https://github.com/user-attachments/assets/db309eee-eb8d-4b6b-9077-3b4fbf3cd4a4" />


<br>**Çalıştırılması:**<br>

* Repo'yu indirdikten sonra gui.py dosyasındaki 107.kod satırındaki cascade değişkenine cascade.xml dosya yolunuzu yazın.<br>
* Bir tane CMD kısa kolu oluşturun ve başlama yeri olarak repoyu indirdiğiniz klasör yolunu yazın sorasında yönetici olarak çalıştırın devamında cd komutu ile klasörünüzün olduğu dizine gidin.<br>
* py -m pip install -r requirements.txt komutu ile önce bütün kütüphanelerin yüklendiğine emin olun ve py gui.py komutu ile farm botunun kullanıcı arayüzünü açın.<br>
* Bulunduğunuz serverdaki map skill barındaki kamerayı saldır olarak değiştirin.<br>
* Arama butonuna basarak açılan selectbox'dan oyun ekranınızı seçin.<br>
* Botun arayüzünden Metin kesme sürenizi yazın ve başlata basın.<br>

Mevcut bot YOLO entegrasyonu yapılarak AI seviyesine çıkarılabilinir. Bot'dan win32ui.error: BitBlt failed hatası alınıyorsa, oyunda ekran yakalama engelli demektir.
Eğer bot çalışıyor, click var ama hareket yok ise bunun %90 sebebi serverda input filter/anti-cheat sistemi vardır. Private serverlar genelde SendInput bloklar sadece düşük seviye input kabul eder. Bu durumda pyautogui/pydirectinput yetersiz kalır, bu durum sadece window focus + raw input injection ile çözülür. Eğer input bloklanıyorsa, Win32 SendInput/ctypes tabanlı Metin2 input bypass sistemi, server’da çalışan gerçek tuş basma motoru ve pyautogui tamamen bypass yapılır.
