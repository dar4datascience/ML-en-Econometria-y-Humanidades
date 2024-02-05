library(dplyr)
library(googlesheets4)

gs4_auth(email = "danielamieva@dar4datascience.com")


write_sheet(
  data = ml_sources_df,
  ss = "https://docs.google.com/spreadsheets/d/1JbUQRjNE4-0O4m3gfx1YEKZ4oXXtv0boDoOX20iPXe0",
  sheet = "raw"
)


read_sheet("https://docs.google.com/spreadsheets/d/1JbUQRjNE4-0O4m3gfx1YEKZ4oXXtv0boDoOX20iPXe0",
           sheet = "raw")