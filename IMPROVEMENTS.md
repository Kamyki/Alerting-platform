# Potencjalne problemy i możliwe usprawnienia

* w bazie danych matchowanie serwisów nie po URL, a po ID, to samo z adminami (nie po imieniu i nazwisku)

* admin-serwis jest na porcie 5000 i działa na gołym flasku. Mieliśmy problemy z uwsgi, które zbierało w jakiś sposób połączenia z mongoDB i nie mogliśmy się dostać do bazy danych

* Przydałby się CI przy użyciu gihub actions

* dostęp do listy monitorowanych serwisów przez API
