----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/26/2021 12:50:35 PM
-- Design Name: 
-- Module Name: fix_address - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity fix_address is

    GENERIC(
       nn_address_output_width              : INTEGER := 7 -- numbers to average over
       );

    Port ( addr_in : in STD_LOGIC_VECTOR (nn_address_output_width-1 downto 0);
           addr_out : out STD_LOGIC_VECTOR (31 downto 0));
end fix_address;

architecture Behavioral of fix_address is
    constant padding    : std_logic_vector(((addr_out'length-1)-(addr_in'length+2)) downto 0) := (others => '0');
begin

    addr_out <= padding & addr_in & "00";

end Behavioral;
