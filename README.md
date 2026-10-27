# SnipeLab PHP2Shell

**PHP2Shell Teknik Analiz ve Kurumsal Savunma Raporu** ile izole doğrulama laboratuvarı.

Kamu ve özel sektörün BT, sistem yönetimi, DevSecOps, SOC ve olay müdahale ekipleri için hazırlanmıştır. Çalışma, PHP çekirdeğindeki yaşam döngüsü sorunlarını açıklar; eski/yamalı/azaltımlı çalışma ortamlarını, etkin ayarları ve normal dosya yüklemesini karşılaştırır.

**SNIPELAB**

Ömer TOKMAK  
Atilla Yusuf Er  
Prof. Dr. Arif SARI  
**Rapor:** 3.1 · **Runtime:** 3.0 · **Dağıtım paketi:** 3.0.6  
**CVE kapsamı:** CVE-2026-109618 ve CVE-2026-109619

## Teknik rapor ve laboratuvar

- [Teknik rapor — PDF](docs/SnipeLab_PHP2Shell_Teknik_Analiz_ve_Kurumsal_Savunma_Raporu.pdf)
- [GitHub üzerinde okunabilir tam metin](docs/SnipeLab_PHP2Shell_Teknik_Analiz_ve_Kurumsal_Savunma_Raporu.md)
- [Laboratuvar kurulum yönergesi](php2shell-lab/README.md)
- [Doğrulama durumu](docs/VALIDATION.md)
- [Kaynaklar ve üçüncü taraf içerik durumu](docs/SOURCES.md)

## Kapsam ve mevcut doğrulama

| Kontrol | Durum |
|---|---|
| Python/HTTP fixture testleri | Kontrol testlerinde 8/8 geçti. |
| Web sürüm ön kontrol testleri | 9/9 geçti; CVE istismarı sınanmadı. |
| Compose YAML ve kaynak yapısı | Ayrıştırma ve yapısal kontroller yapıldı. |
| Gerçek Docker/PHP/Nginx runtime | Kontrol testlerinde çalıştırılmadı; manuel Actions workflow'u sağlandı. |
| WAF/IDS/SIEM | Sensör pakete dahil değil; gerçek alarm kabulü ayrı yapılır. |
| Gerçek PHP UAF/RCE | Bu paketin doğrulama kapsamı değildir. |

Bu araçtaki PASS, seçilmiş kontrol beklentisinin karşılandığını gösterir. Eski hedefin beklenen sürümde çalışması güvenli olduğu anlamına gelmez. OOM veya HTTP 500 tek başına CVE sömürüsü kanıtı değildir.

## Dosya düzeni

| Konum | İçerik |
|---|---|
| `docs/` | PDF ve Markdown teknik rapor, kaynakça ve doğrulama kayıtları |
| `php2shell-lab/app/` | `status.php`, `upload.php`, `oom.php` |
| `php2shell-lab/config/` | PHP INI ve Nginx yapılandırması |
| `php2shell-lab/tools/` | `check.py`, `collect.py`, `lifecycle_model.py` |
| `php2shell-lab/tests/` | Gerçek localhost HTTP fixture testleri |
| `tools/` | Web sürüm ön kontrolü, repo bütünlüğü ve runtime CI yardımcıları |
| `tests/` | Web sürüm ön kontrol aracının dokuz testi |
| `validation/tests/` | Hassas veri içermeyen hazırlama test kayıtları |
| `.github/workflows/` | Otomatik kontroller ve elle başlatılan runtime kontrolü |

## Hızlı başlangıç

Python 3.10+; çalışma için ayrı Ubuntu VM, Docker Engine ve Compose v2 gerekir. Python denetleyici için pip paketi gerekmez. Önce repo kökünde bütünlüğü doğrulayın:

```bash
python3 tools/verify_release.py
python3 -m unittest discover -s php2shell-lab/tests -v
python3 -m unittest discover -s tests -v
```

Laboratuvar servisleri kapalıyken fixture testlerini çalıştırın. Ardından:

```bash
cd php2shell-lab
mkdir -p evidence
docker compose pull apache-old apache-fixed apache-mitigated
python3 tools/collect.py --lock
docker compose --env-file images.lock.env config > evidence/compose-locked.yaml
docker compose --env-file images.lock.env up -d apache-old apache-fixed apache-mitigated
python3 tools/check.py
```

Servis yeni başladıysa ilk kontrol başarısız olabilir; günlükleri kontrol edip servis hazır olduğunda denetleyiciyi yeniden çalıştırın. İmaj değişkenlerini kabukta ayrıca tanımlamayın; çözümlenmiş yapılandırmayı gerçek imajlarla karşılaştırın. `latest` veya bulunmayan etiket yerine sessizce başka sürüm kullanmayın.

FPM, sınırlı OOM, günlük toplama ve kapatma için [laboratuvar README](php2shell-lab/README.md) dosyasını izleyin. Servisler 127.0.0.1'e bağlanır ve internal ağ kullanır. Tanılama endpoint'lerini üretime taşımayın.

## GitHub Actions

`Repository checks`, push ve pull request üzerinde bütünlük/kaynak eşlemesi, Python derleme, fixture testleri, web sürüm ön kontrol testleri ve Compose config kontrolünü çalıştırır. `Runtime verification`, yalnız Actions sayfasından elle başlatılır; imajları alır, PHP lint, Apache/FPM istekleri ve Nginx kontrolünü yürütür. OOM varsayılan olarak kapalıdır.

Workflow dosyasının depoda bulunması testin geçtiği anlamına gelmez. Gerçek çalıştırma sonucu ve artifact'ları esas alın. Başarılı runtime çalışması bile bağımsız UAF/RCE kanıtı değildir.

## Kaynaklar ve lisans

Birincil kaynaklar raporda numaralı olarak gösterilmiştir. Üçüncü taraf araştırma yazıları ve container imajları repo içine kopyalanmamıştır. Bütün repo dosyaları `SHA256SUMS` ile listelenir; bu dosya dijital imza değildir.

Henüz açık lisans atanmamıştır: [LICENSING.md](LICENSING.md). Public erişim ile açık kaynak lisansı aynı şey değildir.

## Web sitesi için sürüm ön kontrolü

Laboratuvar dışında tek bir yetkili URL veya eldeki sürüm dizgesi için `tools/php2shell_version_check.py` kullanılabilir. Bu araç istismar testi yapmaz ve SAFE sonucu üretmez.
