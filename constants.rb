require 'csv'
require 'open-uri'

File.open('constants.py', 'w') do |f|
  f.write "# coding: utf-8\n"
  f.write "names = {}\n"
  f.write "subdivisions = {}\n"
  f.write "styles = {u'ocd-division/country:ca': [u'MP']}\n"

  names = {}

  %w(ca_provinces_and_territories ca_census_divisions ca_census_subdivisions).each do |filename|
    rows = CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv"))
    rows.shift
    rows.each do |id,name|
      names[id] = name
      f.write %(names[u'#{id}'] = u"#{name}"\n)
    end
  end

  # Federal subdivisions
  f.write %(subdivisions[u'ocd-division/country:ca'] = []\n)
  rows = CSV.parse(open("https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_federal_electoral_districts.csv"))
  rows.shift
  rows.each do |_,name|
    f.write %(subdivisions[u'ocd-division/country:ca'].append(u"#{name}")\n)
  end

  # Provincial subdivisions
  %w(nl pe ns nb qc on mb sk ab bc).each do |type_id|
    f.write %(subdivisions[u'ocd-division/country:ca/province:#{type_id}'] = []\n)
    rows = CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/province-#{type_id}-electoral_districts.csv"))
    rows.shift
    rows.each do |_,name|
      f.write %(subdivisions[u'ocd-division/country:ca/province:#{type_id}'].append(u"#{name}")\n)
    end
  end

  # Territorial subdivisions
  %w(nt).each do |type_id|
    f.write %(subdivisions[u'ocd-division/country:ca/territory:#{type_id}'] = []\n)
    rows = CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/territory-#{type_id}-electoral_districts.csv"))
    rows.shift
    rows.each do |_,name|
      f.write %(subdivisions[u'ocd-division/country:ca/territory:#{type_id}'].append(u"#{name}")\n)
    end
  end

  # Census subdivisions
  rows = CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv'))
  rows.shift
  rows.each do |id,name|
    f.write %(subdivisions[u'#{id}'] = [u"#{name}"]\n)
  end

  # Municipal subdivisions
  rows = CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_municipal_subdivisions.csv'))
  rows.shift
  rows.each do |id,name|
    identifier, _, pair = id.rpartition('/')
    f.write %(subdivisions[u'#{identifier}'].append(u"#{name}")\n)
    if pair[/:\d+\z/] # Alternate number-based names
      alternate_name = pair.capitalize.sub(':', ' ')
      f.write %(subdivisions[u'#{identifier}'].append(u"#{alternate_name}")\n) unless name == alternate_name
    end
  end

  seen = {}
  rows = CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_municipal_subdivisions-parent_id.csv'))
  rows.shift
  rows.sort_by(&:last).each do |id,parent_id|
    unless seen.key?(parent_id)
      f.write %(subdivisions[u'#{parent_id}'] = []\n)
      seen[parent_id] = true
    end
    f.write %(subdivisions[u'#{parent_id}'].append(u"#{names.fetch(id)}")\n)
  end

  headers = ['Leader', 'Deputy Leader', 'Member', 'Member At Large']

  [0, 1, 2].each do |gid|
    CSV.parse(open("https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=#{gid}&output=csv"), headers: true) do |row|
      if headers.any?{|header| row[header]}
        f.write "styles[u'#{row['Identifier']}'] = []\n"
        headers.each do |header|
          f.write %(styles[u'#{row['Identifier']}'].append(u"#{row[header]}")\n) if row[header]
        end
      end
    end
  end
end
