
Poniższa instrukcja opisuje "symulację" systemu krok po kroku.
Domyślnie całość działa jako job-scheduler na Kubernetesie, jednak jego konfiguracja może być problematyczna, dlatego niżej pokazujemy krok po kroku co się dzieje, z możliwością łatwej reprodukcji.


* ustaw zmieną `export ALERTING_SECRET_PATH=/twoja/sciezka/secret.yaml`
* niech `secret.yaml` zawiera to co `kubernetes/secret-examle.yml`, tylko jeszcze z ustawionymi poprawnie `db_name` i `db_password`.
* zainstaluj pythonowe zależności: `pip3 install -r worker/requirements.txt`
* na stronie `cloud.mongodb.com` możesz się zalogować mailem `kbz@google.com` - wysłaliśmy zaproszenie, stamtąd można ładnie podglądać zawartość kolekcji (rekordów) bazy danych
* za pomocą skryptu `python3 worker/reset_db.py` możesz zresetować bazę danych i zapełnić ją zawartością plików `admin_api/admins.yaml` i `admin_api/services.yaml`
* w `services.yaml` możesz wstawić swój adres email jako email pierwszego lub drugiego admina i odpalić `reset_db.py`
* tak samo możesz dla testu dodać jakiś nieistniejący/nieodpowiadający url do monitorowania (np. dodając port 21212 do http://www.google.com)
* odpal `python3 worker/worker.py --url <URL do monitorowania`, obecny w services.yaml>
* aby `first_admin` dostał maila, trzeba odpalić powyższy `worker.py` dwa razy (aby przekroczyć `alerting_time`
* powiadomienie do drugiego admina zostanie wysłane, jeśli pierwszy admin nie anuluje incydentu przez `allowed_response_time` (konfigurowalne w pliku `services.yaml`). Wysłaniem powiadomienia do drugiego admina zajmuje się skrypt `worker/reporter.py -- url <URL do monitorowania>`. Jest on schedulowany do `dkron`a przez `worker.py`.
* Do każdego incydentu dla każdego admina zostanie wygenerowany jednorazowy token do autoryzacji anulowania. Na podanego w konfiguracji maila przyjdzie powiadomienie z treścią polecenia, które należy uruchomić w folderze `admin_api` (będzie to uruchomienie `python3 admin_cancel_incident.py <argumenty>`, gdzie argumenty to popsuty URL, jednorazowy token i endpoint serwera anulowania (opis niżej).
* serwer anulowania należy uruchomić za pomocą `admin_api/run_admin_incident_endpoints.sh` (domyślnie jest on częścią klastra), po otrzymaniu zapytania od `admin_cancel_incident.py` anuluje on wybrany incydent.
* stan incydentu (i wszystko inne) można podejrzeć na GUI bazy danych `cloud.mongodb.com`. atrybut `active` jest True, dopóki któryś admin nie anuluje incydentu.
