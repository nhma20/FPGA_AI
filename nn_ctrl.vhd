----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/08/2021 12:17:41 PM
-- Design Name: 
-- Module Name: nn_ctrl - Behavioral
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

entity nn_ctrl is
    Port (  i_Clk : in STD_LOGIC;
            ap_ready : in STD_LOGIC;
            ap_start : out STD_LOGIC;
            
            nn_res_in: in  std_logic_vector(31 downto 0);
           
            input_img_0 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_1 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_2 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_3 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_4 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_5 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_6 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_7 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_8 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_9 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_10 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_11 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_12 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_13 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_14 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_15 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_16 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_17 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_18 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_19 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_20 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_21 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_22 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_23 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_24 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_25 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_26 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_27 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_28 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_29 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_30 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_31 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_32 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_33 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_34 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_35 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_36 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_37 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_38 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_39 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_40 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_41 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_42 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_43 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_44 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_45 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_46 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_47 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_48 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_49 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_50 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_51 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_52 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_53 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_54 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_55 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_56 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_57 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_58 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_59 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_60 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_61 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_62 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_63 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_64 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_65 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_66 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_67 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_68 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_69 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_70 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_71 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_72 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_73 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_74 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_75 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_76 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_77 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_78 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_79 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_80 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_81 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_82 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_83 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_84 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_85 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_86 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_87 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_88 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_89 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_90 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_91 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_92 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_93 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_94 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_95 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_96 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_97 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_98 : OUT STD_LOGIC_VECTOR (31 downto 0);
            input_img_99 : OUT STD_LOGIC_VECTOR (31 downto 0)
           
           );
end nn_ctrl;

architecture Behavioral of nn_ctrl is

    signal start_signal :   std_logic := '0';
    type ROM is array (99 downto 0) of STD_LOGIC_VECTOR(31 downto 0);
    constant image_vals :   ROM := ("00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000", "00111100100000001000000010000001", "00111100000000001000000010000001", "00111100000000001000000010000001", "00111100100000001000000010000001", "00111100000000001000000010000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00111011100000001000000010000001", "00111100010000001100000011000001", "00111011100000001000000010000001", "00111100110000001100000011000001", "00111100100000001000000010000001", "00111100000000001000000010000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000", "00111100010000001100000011000001", "00111110100011001000110010001101", "00111111001010101010101010101011", "00111110101001101010011010100111", "00111100100000001000000010000001", "00111100100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00111011100000001000000010000001", "00111110110001001100010011000101", "00111110111111001111110011111101", "00111110101110001011100010111001", "00111111000011111000111110010000", "00111100101000001010000010100001", "00111100000000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00111101101110001011100010111001", "00111111000111001001110010011101", "00111100111000001110000011100001", "00111110100001101000011010000111", "00111111010001011100010111000110", "00111100111000001110000011100001", "00111100010000001100000011000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00111101101010001010100010101001", "00111111001111111011111111000000", "00111110110001001100010011000101", "00111111001001011010010110100110", "00111111000101001001010010010101", "00111100010000001100000011000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00111011100000001000000010000001", "00111110001100001011000010110001", "00111110110001101100011011000111", "00111110101000101010001010100011", "00111110110110001101100011011001", "00111100000000001000000010000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000", "00111100010000001100000011000001", "00111100010000001100000011000001", "00111110110110101101101011011011", "00111110110100001101000011010001", "00111100000000001000000010000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000", "00111100000000001000000010000001", "00111100000000001000000010000001", "00111111000100001001000010010001", "00111110100010101000101010001011", "00111100010000001100000011000001", "00111011100000001000000010000001", "00000000000000000000000000000000", 
"00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000", "00111100100000001000000010000001", "00111100100000001000000010000001", "00111110001101001011010010110101", "00111101100110001001100010011001", "00111100010000001100000011000001", "00111100000000001000000010000001", "00000000000000000000000000000000");

begin

    PROCESS(i_Clk, start_signal)
      VARIABLE cnt : INTEGER := 0;
    BEGIN
        if rising_edge(i_Clk) then
            if cnt < 101 then
                cnt := cnt + 1;
            end if;
        end if;
        
        if cnt > 100 then
            if ap_ready = '1' then
                start_signal <= '1';
            end if;
        end if;
    END PROCESS;

    ap_start <= start_signal;

    input_img_0  <= image_vals(0);
    input_img_1  <= image_vals(1); 
    input_img_2  <= image_vals(2);
    input_img_3  <= image_vals(3);
    input_img_4  <= image_vals(4);
    input_img_5  <= image_vals(5);
    input_img_6  <= image_vals(6);
    input_img_7  <= image_vals(7);
    input_img_8  <= image_vals(8);
    input_img_9  <= image_vals(9);
    input_img_10  <= image_vals(10);
    input_img_11  <= image_vals(11);
    input_img_12  <= image_vals(12);
    input_img_13  <= image_vals(13);
    input_img_14  <= image_vals(14);
    input_img_15  <= image_vals(15);
    input_img_16  <= image_vals(16);
    input_img_17  <= image_vals(17);
    input_img_18  <= image_vals(18);
    input_img_19  <= image_vals(19);
    input_img_20  <= image_vals(20);
    input_img_21  <= image_vals(21);
    input_img_22  <= image_vals(22);
    input_img_23  <= image_vals(23);
    input_img_24  <= image_vals(24);
    input_img_25  <= image_vals(25);
    input_img_26  <= image_vals(26);
    input_img_27  <= image_vals(27);
    input_img_28  <= image_vals(28);
    input_img_29  <= image_vals(29);
    input_img_30  <= image_vals(30);
    input_img_31  <= image_vals(31);
    input_img_32  <= image_vals(32);
    input_img_33  <= image_vals(33);
    input_img_34  <= image_vals(34);
    input_img_35  <= image_vals(35);
    input_img_36  <= image_vals(36);
    input_img_37  <= image_vals(37);
    input_img_38  <= image_vals(38);
    input_img_39  <= image_vals(39);
    input_img_40  <= image_vals(40);
    input_img_41  <= image_vals(41);
    input_img_42  <= image_vals(42);
    input_img_43  <= image_vals(43);
    input_img_44  <= image_vals(44);
    input_img_45  <= image_vals(45);
    input_img_46  <= image_vals(46);
    input_img_47  <= image_vals(47);
    input_img_48  <= image_vals(48);
    input_img_49  <= image_vals(49);
    input_img_50  <= image_vals(50);
    input_img_51  <= image_vals(51);
    input_img_52  <= image_vals(52);
    input_img_53  <= image_vals(53);
    input_img_54  <= image_vals(54);
    input_img_55  <= image_vals(55);
    input_img_56  <= image_vals(56);
    input_img_57  <= image_vals(57);
    input_img_58  <= image_vals(58);
    input_img_59  <= image_vals(59);
    input_img_60  <= image_vals(60);
    input_img_61  <= image_vals(61);
    input_img_62  <= image_vals(62);
    input_img_63  <= image_vals(63);
    input_img_64  <= image_vals(64);
    input_img_65  <= image_vals(65);
    input_img_66  <= image_vals(66);
    input_img_67  <= image_vals(67);
    input_img_68  <= image_vals(68);
    input_img_69  <= image_vals(69);
    input_img_70  <= image_vals(70);
    input_img_71  <= image_vals(71);
    input_img_72  <= image_vals(72);
    input_img_73  <= image_vals(73);
    input_img_74  <= image_vals(74);
    input_img_75  <= image_vals(75);
    input_img_76  <= image_vals(76);
    input_img_77  <= image_vals(77);
    input_img_78  <= image_vals(78);
    input_img_79  <= image_vals(79);
    input_img_80  <= image_vals(80);
    input_img_81  <= image_vals(81);
    input_img_82  <= image_vals(82);
    input_img_83  <= image_vals(83);
    input_img_84  <= image_vals(84);
    input_img_85  <= image_vals(85);
    input_img_86  <= image_vals(86);
    input_img_87  <= image_vals(87);
    input_img_88  <= image_vals(88);
    input_img_89  <= image_vals(89);
    input_img_90  <= image_vals(90);
    input_img_91  <= image_vals(91);
    input_img_92  <= image_vals(92);
    input_img_93  <= image_vals(93);
    input_img_94  <= image_vals(94);
    input_img_95  <= image_vals(95);
    input_img_96  <= image_vals(96);
    input_img_97  <= image_vals(97);
    input_img_98  <= image_vals(98);
    input_img_99  <= image_vals(99);
    
end Behavioral;

