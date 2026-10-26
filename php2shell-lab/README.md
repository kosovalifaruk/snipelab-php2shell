# SnipeLab PHP2Shell teknik doğrulama paketi

Bu paket kamu ve özel sektör BT, sistem yönetimi, DevSecOps, SOC ve olay müdahale ekipleri için hazırlanmıştır. Gerçek PHP çalışma ortamının sürüm, SAPI, etkin yapılandırma ve normal dosya yükleme davranışını ölçer. `lifecycle_model.py`, durum ömrü hatasını soyut bir modelde görünür kılar. Model ve OOM gözlemi gerçek PHP UAF/RCE PoC'si değildir.

## Gereksinimler

Ayrı Ubuntu VM, Docker Engine, Compose v2, Python 3.10+ ve curl. Önerilen kapasite 4 vCPU, 8 GB RAM, 20 GB disk; GPU gerekmez. Bu değerler planlama önerisidir. İmajlar ilk hazırlıkta internetten alınır. Servisler yalnız loopback'e yayımlanır; Docker ağı internaldir. Bu portları tünelle veya port yönlendirmeyle dışarı açmayın.

## Başlatma

Paket kökünde çalışın:

```bash
mkdir -p evidence
docker compose config > evidence/compose-before-lock.yaml
docker compose pull apache-old apache-fixed apache-mitigated
python3 tools/collect.py --lock
docker compose --env-file images.lock.env config > evidence/compose-locked.yaml
docker compose --env-file images.lock.env up -d apache-old apache-fixed apache-mitigated
python3 tools/check.py
```

`images.lock.env` yerelde çekilen imajın gerçek RepoDigest değerlerinden üretilir. İmaj bulunamazsa veya digest yoksa işlem durur. Alternatif etikete sessizce geçilmez. Bu paket önceden doğrulanmış bir imaj digest'i iddia etmez. Sürümler eski/yamalı karşılaştırma çiftidir; üretim için güncel sağlayıcı paketi gerekir.

## İsteğe bağlı gözlemler

```bash
python3 tools/lifecycle_model.py > evidence/lifecycle-model.json
python3 tools/check.py --oom-demo
docker compose --env-file images.lock.env logs --no-color > evidence/runtime.log
docker stats --no-stream > evidence/resources.txt
```

OOM isteği sabit 24 MiB tahsis dener ve uygulama limitini 16M yapar. Dinamik tahsis boyutu alınmaz. `oom_confirmed=false`, günlük korelasyonunun otomatik yapılmadığını belirtir. HTTP 500/bağlantı kesilmesi tek başına OOM veya CVE kanıtı değildir. Günlükte LAB_BOUNDED_OOM_DEMO ve ilgili fatal hata/işçi çıkışını birlikte inceleyin.

## İsteğe bağlı FPM

```bash
docker compose --profile fpm pull
python3 tools/collect.py --fpm --lock
docker compose --env-file images.lock.env --profile fpm up -d
docker compose --env-file images.lock.env exec -T gateway nginx -t
python3 tools/check.py --fpm
```

18081/18082/18083 Apache eski/yamalı/azaltımlı; 18084/18085 FPM eski/yamalıdır. FPM 9000 ana makineye yayımlanmaz. Nginx 1.28.0-alpine yalnız tekrarlanabilir laboratuvar seçimi içindir; üretim önerisi değildir. Çekme sonrası digest ile sabitleyin.

## Tespit ve kapsam

Paket WAF/IDS kurmaz. Mevcut test sensöründe küçük PHP_SESSION_UPLOAD_PROGRESS işaretçisi ve normal yükleme birlikte sınanabilir. İstek yolu sensörden geçmiyorsa alarm beklenmez. İmza eşleşmesi zafiyetin sömürüldüğünü göstermez. Topluluk kuralları bu pakete doğrulanmış ürün kuralı olarak gömülmemiştir.

## Kontrol aracı testi

Servisleri kapattıktan sonra:

```bash
python3 -m unittest discover -s tests -v
```

Bu testler beş yerel HTTP fixture'ı açar. PHP/Docker yerine geçmez; sürüm uyuşmazlığı, bozuk yükleme özeti ve yönlendirme reddi gibi denetleyici davranışlarını sınar. 18081–18085 boş olmalıdır. Sonuçlar VALIDATION.md içinde ayrılır.

## Kapatma

```bash
docker compose --env-file images.lock.env --profile fpm logs --no-color > evidence/final.log
docker compose --env-file images.lock.env --profile fpm ps -a > evidence/final-containers.txt
docker compose --env-file images.lock.env --profile fpm down
```

Tanılama ve OOM endpoint'lerini üretime taşımayın. Kanıtlar hassas ortam bilgisi içerebilir; erişim ve saklama politikasını kurum belirler. SHA256SUMS aktarım bütünlüğü kontrolüdür, yayıncının dijital imzası değildir.
