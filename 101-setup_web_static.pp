# Define a custom fact to check if the directory exists
Facter.add('web_static_dir_exists') do
  setcode do
    File.exist?('/data/web_static')
  end
end

# Create the /data directory if it doesn't exist
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
}

# Create the /data/web_static directory if it doesn't exist
if $web_static_dir_exists == false {
  file { '/data/web_static':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0755',
  }
}

# Create the /data/web_static/releases directory if it doesn't exist
file { '/data/web_static/releases':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data/web_static'],
}

# Create the /data/web_static/releases/test directory if it doesn't exist
file { '/data/web_static/releases/test':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => File['/data/web_static/releases'],
}

# Create the symbolic link /data/web_static/current
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test'],
}

# Create the HTML file /data/web_static/releases/test/index.html
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  require => File['/data/web_static/releases/test'],
}

# Define an Apache vhost for hbnb_static
apache::vhost { 'hbnb_static':
  docroot     => '/data/web_static/current',
  port        => '80',
  servername  => 'localhost',
  serveradmin => 'webmaster@localhost',
  require     => File['/data/web_static/current'],
}
