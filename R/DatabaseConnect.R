#Have to follow this to install drivers for psql
#https://db.rstudio.com/best-practices/drivers/

# Install the latest odbc release from CRAN:
install.packages("odbc")

# Or the the development version from GitHub:
# install.packages(devtools)
devtools::install_github("rstats-db/odbc")



con <- DBI::dbConnect(odbc::odbc(),
                      Driver   = "odbc",
                      Server   = "139.147.9.145",
                      Database = "stride_db",
                      UID      = "public_reader",
                      PWD      = rstudioapi::askForPassword("public_reader password"),
                      Port     = 5432)