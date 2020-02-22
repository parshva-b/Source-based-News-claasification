const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const morgan = require('morgan')
const cors = require('cors')

const newsRouter = require('./controllers/routes')
const middleware = require('./utils/middleware')

app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
morgan.token('body', function(res, req) { return JSON.stringify( req.body ) })
app.use(morgan(':method :url :status :res[content-length] - :response-time ms :body'))

app.use('/', newsRouter)

app.use(middleware.unknownEndpoint)
app.use(middleware.errorHandler)

module.exports = app