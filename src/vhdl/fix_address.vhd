----------------------------------------------------------------------------------
-- Company: SDU, UAS, DIII
-- Engineer: Nicolaj Malle
-- 
-- Create Date: 10/26/2021 12:50:35 PM
-- Project Name: FPGA_AI
-- Target Devices: PYNQ-Z2
-- Tool Versions: 2021.1
-- Description: Aligns nn_inference IP module output address with BRAM
-- input address
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fix_address is

    GENERIC(
       nn_address_output_width              : INTEGER := 7
       );

    Port ( addr_in : in STD_LOGIC_VECTOR (nn_address_output_width-1 downto 0);
           addr_out : out STD_LOGIC_VECTOR (31 downto 0));
end fix_address;

architecture Behavioral of fix_address is
    constant padding    : std_logic_vector(((addr_out'length-1)-(addr_in'length+2)) downto 0) := (others => '0');
begin

    addr_out <= padding & addr_in & "00";

end Behavioral;
