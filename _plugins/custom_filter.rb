
module DateFilter
  MONTHS = %w(Janvier Février Mars Avril Mai Juin Juillet Août Septembre Octobre Novembre Décembre)

  def month_fr(input)

    return input unless (date = Liquid::Utils.to_date(input))

    MONTHS[date.strftime("%m").to_i - 1]
  end
end

Liquid::Template.register_filter(DateFilter)
