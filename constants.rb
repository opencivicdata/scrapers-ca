require 'csv'
require 'open-uri'

File.open('constants.py', 'w') do |f|
  f.write "# coding: utf-8\n"
  f.write "names = {}\n"
  f.write "subdivisions = {}\n"
  f.write "styles = {u'ocd-division/country:ca': [u'MP']}\n"

  %w(ca_provinces_and_territories ca_census_divisions ca_census_subdivisions).each do |filename|
    rows = CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/#{filename}.csv"))
    rows.shift
    rows.each do |row|
      f.write %(names[u'#{row[0]}'] = u"#{row[1]}"\n)
    end
  end

  %w(pe ns nb qc on mb sk ab bc).each do |type_id|
    f.write %(subdivisions[u'ocd-division/country:ca/province:#{type_id}'] = []\n)
    rows = CSV.parse(open("https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/province-#{type_id}-electoral_districts.csv"))
    rows.shift
    rows.each do |row|
      f.write %(subdivisions[u'ocd-division/country:ca/province:#{type_id}'].append(u"#{row[1]}")\n)
    end
  end

  rows = CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv'))
  rows.shift
  rows.each do |row|
    f.write %(subdivisions[u'#{row[0]}'] = [u"#{row[1]}"]\n)
  end

  rows = CSV.parse(open('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_municipal_subdivisions.csv'))
  rows.shift
  rows.each do |row|
    identifier, _, pair = row[0].rpartition('/')
    f.write %(subdivisions[u'#{identifier}'].append(u"#{row[1]}")\n)
    if pair[/:\d+\z/]
      alternative_name = pair.capitalize.sub(':', ' ')
      f.write %(subdivisions[u'#{identifier}'].append(u"#{alternative_name}")\n) unless row[1] == alternative_name
    end
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
