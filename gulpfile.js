'use strict';

//Deklaracje zmiennych
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const autoprefixer = require('gulp-autoprefixer');

//Funkcja testowa
async function hello() {
	return console.log("Hello Zeton's Team");	
};

//Funkcje
function compile () {
    return gulp.src('./zeton/static/sass/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
        browsers: ['last 99 versions'],
        cascade: false
}))    
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./zeton/static/css'));
}

function watch () {
    gulp.watch('./zeton/static/sass/**/*.scss', compile);
}

exports.hello = hello;
exports.compile = compile;
exports.watch = watch;