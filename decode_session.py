import base64, json, zlib
token = "eJwlzrsRwjAMANBdVKewZMWWWCYn63PQJqTi2J2CN8H7wFFnXk94vM87NzheAQ_oSstYjLjUi50ww8O5jSbcu49oRbuoTerLK02UE9scIlOkeVup6rXGpOR91BQ39YlEEeYxOmIpqWGm7OVkJsY5CNdqE8Vgg-O-8vxvEL4_4d8v1A.adjBdw.BwlWSSV4LFaFIw3TNrHoLrVdOKY"
payload = token.split('.')[0]
padding = 4 - len(payload) % 4
payload += '=' * padding

decoded = base64.urlsafe_b64decode(payload)

# 去掉開頭的 . 並解壓縮
result = zlib.decompress(decoded)
print(json.loads(result))