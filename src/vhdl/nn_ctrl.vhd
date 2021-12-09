----------------------------------------------------------------------------------
-- Company: SDU, UAS, DIII
-- Engineer: Nicolaj Malle
-- 
-- Create Date: 10/08/2021 12:17:41 PM
-- Project Name: FPGA_AI
-- Target Devices: PYNQ-Z2
-- Tool Versions: 2021.1
-- Description: Starts nn_inference IP module and outputs inference results
-- on  PYNQ-Z2 board LEDs.
----------------------------------------------------------------------------------



library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity nn_ctrl is
    Port (  i_Clk : in STD_LOGIC;
            ap_ready : in STD_LOGIC;
            ap_start : out STD_LOGIC;
            ap_done  : in std_logic;
            ap_idle  : in std_logic;
            ap_rst   : out std_logic;
            rstb_busy: in std_logic;
            
            led_ctrl1: out std_logic;
            led_ctrl2: out std_logic;
            led_ctrl3: out std_logic;
            led_ctrl4: out std_logic;
            
            nn_res_in: in  std_logic_vector(31 downto 0)
           
           );
end nn_ctrl;

architecture Behavioral of nn_ctrl is

    signal start_signal :   std_logic := '0';
    signal s_led_ctrl1  :   std_logic := '0';
    signal s_led_ctrl2  :   std_logic := '0';  
    signal s_led_ctrl3  :   std_logic := '0';
    signal s_led_ctrl4  :   std_logic := '0';
    
    signal led_ctrl     :   std_logic_vector(3 downto 0);
    
    signal pred         :   integer := 0;
    
begin

    ------------------  Start NN  ------------------
    PROCESS(i_Clk, start_signal)
      VARIABLE cnt : INTEGER := 0;
    BEGIN
        if rising_edge(i_Clk) then
            if cnt < 3 then
                cnt := cnt + 1;
            end if;
        end if;
        
        if cnt > 2 then
            if ap_ready = '1' or ap_idle = '1' then
                if rstb_busy = '0' then
                    start_signal <= '1';
                else 
                    start_signal <= '0';
                end if;
            end if;
        end if;
    END PROCESS;


    pred <= to_integer(signed(nn_res_in));

    with pred select led_ctrl <=
        "0001" when 1,
        "0010" when 2,
        "0011" when 3,
        "0100" when 4,
        "0101" when 5,
        "0110" when 6,
        "0111" when 7,
        "1000" when 8,
        "1001" when 9,
        "1010" when 0,
        "1110" when -1,
        "1111" when 15,
        "0000" when others;
        

    ap_start <= start_signal;

    ap_rst <= '1';
    
    led_ctrl1 <= led_ctrl(0);
    led_ctrl2 <= led_ctrl(1);
    led_ctrl3 <= led_ctrl(2);
    led_ctrl4 <= led_ctrl(3);
    
end Behavioral;
