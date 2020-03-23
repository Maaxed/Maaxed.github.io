
module HashFilter
  def sort_values(input, property = nil)
  	return input.sort_by { |k, v| v[property] }

      # return [] if ary.empty?

      # if property.nil?
      #   ary.sort_by { |k, v| v }
      # else
      #   begin
      #     ary.sort_by { |k, v| v[property] }
      #   rescue TypeError
      #     raise_property_error(property)
      #   end
      # end
    end
end

Liquid::Template.register_filter(HashFilter)