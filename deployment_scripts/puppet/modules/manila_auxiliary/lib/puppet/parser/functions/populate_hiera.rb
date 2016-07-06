module Puppet::Parser::Functions
  newfunction(:populate_hiera,
              :doc => <<-EOS
              Add plugin specific data to hiera.
              EOS
             ) do |args|
    raise(Puppet::ParseError, 'No file name provided!') if args.size < 3 or args[0] == ""
    require 'yaml'
    require 'fileutils'
    file=args[0]
    key=args[1]
    value=args[2]
    begin
      data = YAML::load_file(file)
    rescue
      data = {"manila" => {}}
    end
    data["manila"][key] = value
    File.open(file, 'w') {|f| f.write data.to_yaml}
  end
end
