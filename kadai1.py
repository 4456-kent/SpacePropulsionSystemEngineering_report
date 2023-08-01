# 実行まえにフォートランとRocket CEAをインストール
! apt-get install gfortran
! pip install RocketCEA
# インポート作業
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel, add_new_oxidizer, add_new_propellant
import matplotlib.pyplot as plt
# 設定パラメータ
F = 490 # 推力[N]
g = 9.80665 #重力加速度[m/s^2]
ccp_MPa = 0.4 # 燃焼室圧[MPa]
mr = 0.0
aeat = 100.0 # 開口比
fr = 0 # 0：平衡流，1：凍結流
molefra_area = 1 # 0：噴射口，1：燃焼室，2：スロート，3：ノズル出口

sim = CEA_Obj( oxName='N2O4', fuelName='MMH', pressure_units='MPa',
temperature_units='K', isp_units='sec', cstar_units='m/s',
sonic_velocity_units='m/s', enthalpy_units='J/kg',
density_units='kg/m^3',specific_heat_units='J/kg-K',thermal_cond_units='W/cm-degC' )

# 配列初期化
mr_1 = []
isp_1 = []
cstar_1 = []
Tc_1 = []
N2_1 = []
H2_1 = []
O2_1 = []
CO2_1 = []
CO_1 = []
H2O_1 = []

# プロット部分
for i in range(0, 600):
    mr = i/100.0
    (isp, cstar, tc) = sim.get_IvacCstrTc(Pc = ccp_MPa, MR = mr, eps = aeat, frozen = fr, frozenAtThroat = 0)
    MoleFra = sim.get_SpeciesMoleFractions(Pc = ccp_MPa, MR = mr, eps = aeat, frozen = fr, frozenAtThroat = 0)
    mr_1.append(mr)
    isp_1.append(isp)
    cstar_1.append(cstar)
    Tc_1.append(tc)
    # 燃焼室のモル分率は凍結流と平衡流は一緒で，凍結流におけるモル分率は燃焼室とスロート，ノズル出口で一緒
    if '*N2' in MoleFra[1]:
        N2_1.append(MoleFra[1]['*N2'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        N2_1.append(0.0)

    if '*H2' in MoleFra[1]:
        H2_1.append(MoleFra[1]['*H2'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        H2_1.append(0.0)
    
    if '*O2' in MoleFra[1]:
        O2_1.append(MoleFra[1]['*O2'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        O2_1.append(0.0)

    if '*CO2' in MoleFra[1]:
        CO2_1.append(MoleFra[1]['*CO2'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        CO2_1.append(0.0)

    if '*CO' in MoleFra[1]:
        CO_1.append(MoleFra[1]['*CO'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        CO_1.append(0.0)

    if 'H2O' in MoleFra[1]:
        H2O_1.append(MoleFra[1]['H2O'][molefra_area])   # MoleFra[1][反応種名][0：噴射口，1：燃焼室，2：スロート，3：ノズル出口]
    else:
        H2O_1.append(0.0)

# グラフの描画    
fig = plt.figure(figsize=(20, 5))
isp_ax = fig.add_subplot(1, 4, 1, xlabel = "O/F", ylabel = "Isp, s", title = "Isp") # (行数, 列数, 番号, xlabel, ylabel, title)
isp_ax.set_xlim(0, 6)  # x軸の範囲
isp_ax.set_ylim(0,500)  # y軸の範囲
isp_ax.plot(mr_1, isp_1, 'b')
tc_ax = fig.add_subplot(1, 4, 2, xlabel = "O/F", ylabel = "Temp, K", title = "Adiabatic flame temperature")
tc_ax.set_xlim(0, 6)
tc_ax.set_ylim(0, 3500)
tc_ax.plot(mr_1, Tc_1, 'c')
cstar_ax = fig.add_subplot(1, 4, 3, xlabel = "O/F", ylabel = "Cstar, m/s", title = "C*")
cstar_ax.set_xlim(0,6)
cstar_ax.set_ylim(0,2000)
cstar_ax.plot(mr_1, cstar_1, 'r')
MF_ax = fig.add_subplot(1, 4, 4, xlabel = "O/F", ylabel = "Mole fractions", title = "Molefraction in exit")
MF_ax.set_yscale('log')
MF_ax.plot(mr_1, N2_1, 'g', label = 'N2')
MF_ax.plot(mr_1, H2_1, 'b', label = 'H2')
MF_ax.plot(mr_1, O2_1, 'y', label = 'O2')
MF_ax.plot(mr_1, CO2_1, 'r', label = 'CO2')
MF_ax.plot(mr_1, CO_1, 'm', label = 'CO')
MF_ax.plot(mr_1, H2O_1, 'c', label = 'H2O')
MF_ax.set_xlim(0, 6)
MF_ax.legend()

# 比推力最大になるO/Fとその時の比推力，燃焼室温度，C*の表示
isp_max = max(isp_1)
mr_at_maxisp = isp_1.index(max(isp_1))*0.01
tc_at_maxisp = Tc_1[isp_1.index(max(isp_1))]
cstar_at_maxisp = cstar_1[isp_1.index(max(isp_1))]
print("O/F is %f at the max isp value" % mr_at_maxisp)
print("At that time, Isp = %f s, Tc = %f K, C* = %f m/s" % (isp_max, tc_at_maxisp, cstar_at_maxisp))

# 推進剤流量とスロート断面積，ノズル出口断面積の計算
mdot = F / (isp_max * g) #[kg/s]
At = mdot * cstar_at_maxisp / ccp_MPa # [mm^2]
Ae = At * aeat # [mm^2]

print("Propellant mass flow rate: %f kg/s, Throat cross sectional area: %f mm^2, Nozzle outlet cross sectional area: %f mm^2" % (mdot, At, Ae))