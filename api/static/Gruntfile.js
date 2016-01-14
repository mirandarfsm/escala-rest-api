grunt.initConfig({
    serve: {
        options: {
            port: 9000,
            'client.js': {
                tasks: ['html2js', 'concat'],
                output: 'client.js'
            }
        }
    }
});
