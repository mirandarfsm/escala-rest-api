module.exports = function(grunt){
	grunt.initConfig({
		copy: {
			main: {
        files:[
          {
            expand: true,
    				cwd: '.',
    				src: ['**','!Gruntfile.js','!bower.json','!Dockerfile','!Dockerfile.bkp','!.bowerrc','!package.json','!node_modules'],
    				dest: 'dist'
          },
          {
            expand: true,
            cwd: './vendor/bootstrap/fonts/',
    				src: ['**'],
    				dest: 'dist/fonts/'
          }
        ]
			}
		},
		clean: {
			dist:{
				src: 'dist'
			}
		},
		usemin: {
			html: 'dist/index.html'
		},
		useminPrepare: {
			html: 'dist/index.html'
		},
		ngAnnotate: {
			scripts: {
				expand: true,
				src: ['dist/app/**/*.js']
			}
		}
	});

	grunt.registerTask('default',['dist','minifica']);
	grunt.registerTask('dist',['clean','copy']);
	grunt.registerTask('minifica',['useminPrepare','ngAnnotate','concat','uglify','cssmin','usemin']);

	grunt.loadNpmTasks('grunt-contrib-copy');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-usemin');
	grunt.loadNpmTasks('grunt-ng-annotate');

};
