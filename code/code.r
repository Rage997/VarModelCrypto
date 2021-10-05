library(mvnormtest)
library(gRbase)
library(igraph)
library(lars)
library(psychNET)
library(huge)
library(vars)

# import stock data and plot it
stock <- read.csv("stocks_1h.csv")
stock <- data.matrix(stock)
stock <- log(stock)
# stock <- diff(stock) # if want to use differences
 
par(mfrow=c(1,1))
# DAX    SMI    CAC   FTSE
plot(stock[,4],type="l", main="Uni")

VARselect(stock, 20)


# To check if the system is stable we need to create the companion matrix
# we fit a VAR and then get the coefficients
var <- VAR(stock, lag=2)

coins <- c('BTC', 'ETH', 'UNI', 'ADA', 'BNB', 'CAKE', 'XMR')
# Create companion matrix
# We store it inside a single matrix and will split it
# for each lag, the matrix is given by (lag-1)*n+1 : lag*n
n <- length(coins)
#Now we have a matrix which contains all the companion matrices in a single matrix
eye<-diag(n)
empty <- diag(numeric(n))
tmp <- cbind(eye,empty)
c = coef(var)
res = lapply(c, function(x)x[,1])
str(res)
res = matrix(unlist(res), nrow=7, byrow=T)
res_mat <- rbind(res[, 1:14], tmp)
#res_mat <- res[, 1:7]
abs(eigen(res_mat)$values) #eigenvalues are close to 1!
 
var3<-psychNET(stock, "GVAR", criterion = "EBIC",penalty="LASSO", lag=2)
#summary(var3)
#plot(plot(var3)[[1]]$igraph)

p<-ncol(stock)
n<-nrow(stock)-1 
# n coins = 7
A1 = t(var3$fit$beta[, 2:8])
A2 = t(var3$fit$beta[, 9:15])

# Plot data
png("/home/rage/Desktop/4st_semester/graphical_models/assignments/project/report 2/images/var_model1.png",
    width     = 3.25,
    height    = 3.25,
    units     = "in",
    res       = 1200,
    pointsize = 4)
par(mfrow=c(1,1))
adj<-1*(A1!=0)
colnames(adj) = colnames(stock)[1:p]
rownames(adj) = colnames(stock)[1:p]
g<-graph_from_adjacency_matrix(adj)
plot(g)
dev.off()

png("/home/rage/Desktop/4st_semester/graphical_models/assignments/project/report 2/images/var_model2.png",
    width     = 3.25,
    height    = 3.25,
    units     = "in",
    res       = 1200,
    pointsize = 4)
par(mfrow=c(1,1))
adj<-1*(A2!=0)
colnames(adj) = colnames(stock)[1:p]
rownames(adj) = colnames(stock)[1:p]
g<-graph_from_adjacency_matrix(adj)
plot(g)
dev.off() 
