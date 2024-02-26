from upbitlib import upbit

access_key = "YOUR_ACCESS_KEY"
secret_key = "YOUR_SECRET_KEY"

upbit = upbit.Upbit(access_key, secret_key)

print(upbit.get_markets())
