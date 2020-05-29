
module HashFilter
  def sort_values(input, property = nil)
    if property.nil?
      return input.sort { |a, b| nil_safe_compare(a[1], b[1]) }
    else
      begin
        return input.sort { |a, b| nil_safe_compare(a[1][property], b[1][property]) }
      rescue TypeError
        raise_property_error(property)
      end
    end
  end

  def reversed(input)
    input.reverse
  end

  private

  def nil_safe_compare(a, b)
    if !a.nil? && !b.nil?
      a <=> b
    else
      a.nil? ? 1 : -1
    end
  end
  def raise_property_error(property)
    raise Liquid::ArgumentError, "cannot select the property '#{property}'"
  end
end

Liquid::Template.register_filter(HashFilter)