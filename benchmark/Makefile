bench-redis:
	@ locust -f benchmark_redis.py --headless -u 100 -r 10 --run-time 1m --host=localhost --csv-full-history --csv bench.csv

bench-postgres:
	@ locust -f benchmark_postgres.py --headless -u 100 -r 10 --run-time 5m --host=localhost --csv-full-history --csv bench.csv

bench-zeon:
	@ locust -f benchmark_zeon.py --headless -u 100 -r 10 --run-time 30s --host=localhost --csv-full-history --csv bench.csv

