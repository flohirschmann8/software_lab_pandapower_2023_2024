

import pandapower as pp

net = pp.create_empty_network()
pp.create_bus(net, 20)
pp.create_bus(net, 0.4)
pp.create_bus(net, 0.4)
pp.create_ext_grid(net,bus=0,vm_pu=1.02)


pp.create_load(net, bus=2,p_mw=0.1)
pp.create_transformer_from_parameters(net, hv_bus=0,lv_bus=1 ,sn_mva=1, vn_hv_kv=20,vn_lv_kv=0.4,vkr_percent=1.425,vk_percent=6,pfe_kw=1.35,i0_percent=0.3375)
pp.create_sgen(net,2,0.1)
pp.create_line(net,from_bus=1,to_bus=2,length_km=0.1, std_type='NAYY 4x50 SE')


pp.runpp(net)

