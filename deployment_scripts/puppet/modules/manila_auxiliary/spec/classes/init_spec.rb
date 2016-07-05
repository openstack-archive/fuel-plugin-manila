require 'spec_helper'
describe 'manila_auxiliary' do

  context 'with defaults for all parameters' do
    it { should contain_class('manila_auxiliary') }
  end
end
