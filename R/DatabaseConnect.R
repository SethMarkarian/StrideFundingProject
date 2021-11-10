# Have to follow this to install drivers for psql
# https://db.rstudio.com/best-practices/drivers/
# https://www.youtube.com/watch?v=vchmuyLzjkg

# Install the latest odbc release from CRAN:
install.packages("odbc")

# Or the the development version from GitHub:
# install.packages(devtools)
devtools::install_github("rstats-db/odbc")

library(DBI)
library(RODBC)
library(odbc)


con <- DBI::dbConnect(odbc::odbc(),"psqlR")
data <- dbGetQuery(con, 'SELECT * FROM school_career_outcomes')