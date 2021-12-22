import osimport csvimport numpy  as npimport pandas as pdimport matplotlib.pyplot as pltfrom math import log10, floor# Run From Either PostIrrad or PreIrrad# Is NaN Functiondef isNaN(num):    return num != num# Significant Figures Functiondef round_sig(x, sig=6, small_value=1.0e-9):    if isNaN(x) == True:        return x    else:        return round(x, sig - int(floor(log10(max(abs(x), abs(small_value))))) - 1)    def make_df(headers, array):    temp_dataframe = {}    array_shape = array.shape    array_width = array_shape[1]    array_len = array_shape[0]        for i in range(0,array_len):                temp_dataframe[headers[i]] = np.zeros(array_width).reshape(array_width)                for j in range(0, array_width):                        temp_dataframe[headers[i]][j] = array[i,j]                df = pd.DataFrame(temp_dataframe,index=['I(600V)', 'I(800V)', 'I(1000V)', 'DepV'])    df = df.transpose()        return df# Diode Names for Plotting diode_names_preirrad = ['IRRADSENSOR', 'DIODE', 'DIODEHALF', 'DIODEHALFPSTOP', 'DIODEHALFPSTOP_GR', 'DIODEQUARTER']diode_names_postirrad = ['DIODE', 'DIODEHALF', 'DIODEHALFPSTOP', 'DIODEHALFPSTOP_GR', 'DIODEQUARTER', 'IRRADSENSOR_20min', 'IRRADSENSOR_1100min']current_color = ["red", "blue", "green"]table_label = ['I(600V)', 'I(800V)', 'I(1000V)', 'DepV']scale_factor = [10**6, 10**9]# Current Working Directorycwd = os.getcwd()# Convert .txt File to .csv Filedef txt_to_csv(file):    with open(str(file)+'.txt') as fin, open(str(file)+'.csv', 'w') as fout:        for line in fin:            fout.write(line.replace('\t', ','))# List all of the Files in the Current Working Directory search_path = '.'   # set your path here.root, dirs, files = next(os.walk(search_path), ([],[],[]))# Organize dirs (Directories)dirs = sorted(dirs)#%%# Find the Number of Each Diodenum_DIODE = 0num_HALF = 0num_PSTOP = 0num_GR = 0num_QUARTER = 0num_IRRADSENSOR = 0num_IRRADSENSOR_20min = 0num_IRRADSENSOR_1100min = 0for i in range(0, len(dirs)):        # Organize sub_dirs (Sub Directories)    sub_root, sub_dirs, sub_files = next(os.walk(dirs[i]), ([],[],[]))    sub_dirs = sorted(sub_dirs)        # Make a path for each sub diode id, use this to get to the table with the current values    for j in range(0, len(sub_dirs)):           path = str(dirs[i])+'/' + str(sub_dirs[j])+'/CumulData'        print(path)        txt_to_csv(path)        CumulData = pd.read_csv(path + '.csv')        for k in range(0,len(CumulData['File'])):                                        if "QUARTER" in CumulData['File'][k]:                 num_QUARTER += 1                                        elif "GR" in CumulData['File'][k]:                 num_GR += 1                                            elif "PSTOP" in CumulData['File'][k]:                 num_PSTOP += 1                            elif "HALF" in CumulData['File'][k]:                 num_HALF += 1                            elif "DIODE" in CumulData['File'][k]:                 num_DIODE += 1                             if "PreIrrad" in cwd:                                 if "IRRADSENSOR" in CumulData['File'][k]:                     num_IRRADSENSOR += 1                            elif "20min" in CumulData['File'][k]:                 num_IRRADSENSOR_20min += 1                            elif "1100min" in CumulData['File'][k]:                 num_IRRADSENSOR_1100min += 1# Iterate Over All The Files, Begin Creating Graphs diodes = {}diode = {}half = {}pstop = {}gr = {}quarter = {}irradsensor = {}irradsensor_20min = {}irradsensor_1100min = {}# Names of Diodesdiodes_name = []diode_name = []half_name = []pstop_name = []gr_name = []quarter_name = []irradsensor_name = []irradsensor_20min_name = []irradsensor_1100min_name = []# Reshape to the Size of the Necessary Vectordiode = np.zeros(num_DIODE*4).reshape(num_DIODE,4)half = np.zeros(num_HALF*4).reshape(num_HALF,4)pstop = np.zeros(num_PSTOP*4).reshape(num_PSTOP,4)gr = np.zeros(num_GR*4).reshape(num_GR,4)quarter = np.zeros(num_QUARTER*4).reshape(num_QUARTER,4)irradsensor = np.zeros(num_IRRADSENSOR*4).reshape(num_IRRADSENSOR,4)irradsensor_20min = np.zeros(num_IRRADSENSOR_20min*4).reshape(num_IRRADSENSOR_20min,4)irradsensor_1100min = np.zeros(num_IRRADSENSOR_1100min*4).reshape(num_IRRADSENSOR_1100min,4)int_DIODE = 0int_HALF = 0int_PSTOP = 0int_GR = 0int_QUARTER = 0int_IRRADSENSOR = 0int_IRRADSENSOR_20min = 0int_IRRADSENSOR_1100min = 0if "PostIrrad" in cwd:     diode_num = 7else:    diode_num = 6        for i in range(0, len(dirs)):    sub_root, sub_dirs, sub_files = next(os.walk(dirs[i]), ([],[],[]))    diodes[dirs[i]] = np.zeros(len(sub_dirs)*diode_num*4).reshape(len(sub_dirs),diode_num,4)    plt.figure(figsize=(10,8))        # Make a path for each sub diode id, use this to get to the table with the current values    for j in range(0, len(sub_dirs)):           path = str(dirs[i])+'/' + str(sub_dirs[j])+'/CumulData'        txt_to_csv(path)        CumulData = pd.read_csv(path + '.csv')        for k in range(0,len(CumulData['File'])):                        # Fill data in dict, do this for as many rows there are in the .csv            for v in range(0,4):                                            if "QUARTER" in CumulData['File'][k]:                     diodes[dirs[i]][j,4,v] = CumulData[table_label[v]][k]                    quarter[int_QUARTER,v] = CumulData[table_label[v]][k]                                           if v == 3:                        quarter_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                        int_QUARTER += 1                                                            elif "GR" in CumulData['File'][k]:                     diodes[dirs[i]][j,3,v] = CumulData[table_label[v]][k]                    gr[int_GR,v] = CumulData[table_label[v]][k]                                           if v == 3:                        gr_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                        int_GR += 1                                                elif "PSTOP" in CumulData['File'][k]:                     diodes[dirs[i]][j,2,v] = CumulData[table_label[v]][k]                    pstop[int_PSTOP,v] = CumulData[table_label[v]][k]                                           if v == 3:                        pstop_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                        int_PSTOP += 1                                elif "HALF" in CumulData['File'][k]:                     diodes[dirs[i]][j,1,v] = CumulData[table_label[v]][k]                    half[int_HALF,v] = CumulData[table_label[v]][k]                                           if v == 3:                        half_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                        int_HALF += 1                                elif "DIODE" in CumulData['File'][k]:                     diodes[dirs[i]][j,0,v] = CumulData[table_label[v]][k]                     diode[int_DIODE,v] = CumulData[table_label[v]][k]                                           if v == 3:                        diode_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                        int_DIODE += 1                                        if "PreIrrad" in cwd:                                            if "IRRADSENSOR" in CumulData['File'][k]:                         diodes[dirs[i]][j,diode_num - 1,v] = CumulData[table_label[v]][k]                         irradsensor[int_IRRADSENSOR,v] = CumulData[table_label[v]][k]                                               if v == 3:                            irradsensor_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                            int_IRRADSENSOR += 1                                        if "PostIrrad" in cwd:                                          if "20min" in CumulData['File'][k]:                         diodes[dirs[i]][j,diode_num - 2,v] = CumulData[table_label[v]][k]                         irradsensor_20min[int_IRRADSENSOR_20min,v] = CumulData[table_label[v]][k]                                               if v == 3:                            irradsensor_20min_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                            int_IRRADSENSOR_20min += 1                                            elif "1100min" in CumulData['File'][k]:                         diodes[dirs[i]][j,diode_num - 1,v] = CumulData[table_label[v]][k]                         irradsensor_1100min[int_IRRADSENSOR_1100min,v] = CumulData[table_label[v]][k]                                               if v == 3:                            irradsensor_1100min_name.append(str(dirs[i]) + '_' + str(sub_dirs[j]))                            int_IRRADSENSOR_1100min += 1        if "PostIrrad" in cwd:             diode_names = diode_names_postirrad            w_num = 7        else:            diode_names = diode_names_preirrad            w_num = 6        for w in range(0,w_num):                        for z in range(0,3):                                # Scale factor depending on whether the diode has been irradiated or not                if "PostIrrad" in cwd:                        factor = scale_factor[0]                        else:                    factor = scale_factor[1]                                # Check to make sure sensible values are in the table                if diodes[dirs[i]][j,w,z] == 0:                    continue                                 if len(sub_dirs[j]) >= 2 and j == 0 and w == 0:                    plt.plot(sub_dirs[j]+'_DIODE',-1*diodes[dirs[i]][j,w,z]*factor, marker=".", markersize=20, color = current_color[z], label = table_label[z])                    plt.subplots_adjust(left=None, bottom=.2, right=None, top=None, wspace=None, hspace=None)                                else:                    plt.plot(sub_dirs[j]+'_'+diode_names[w],-1*diodes[dirs[i]][j,w,z]*factor, marker=".", markersize=20, color = current_color[z])                    plt.subplots_adjust(left=None, bottom=.2, right=None, top=None, wspace=None, hspace=None)                # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated Batch '+dirs[i]+'_HM_XX Diodes', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated Batch '+dirs[i]+'_HM_XX Diodes', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)        # Save all the plots corresponding to the same batch to one .png        plt.savefig(dirs[i]+'.png')    #%%        # Make a table of Depletion Valuesfig, axs = plt.subplots(len(dirs),1)for i in range(0, len(dirs)):    row_labels = []    table_data = []    row_labels = []    temp_array = []     sub_root, sub_dirs, sub_files = next(os.walk(dirs[i]), ([],[],[]))        if "PostIrrad" in cwd:         column_labels = diode_names_postirrad        b_num = 7            else:        column_labels = diode_names_preirrad        b_num = 6                for t in range(0,len(sub_dirs)):        row_labels.append('Batch '+ str(dirs[i]) + '_' +  str(sub_dirs[t]))        temp_array = []        print(row_labels)                   for b in range(0,b_num):            temp_array.append(round_sig(diodes[dirs[i]][t,b,3], 6, 1.0e-9))                 table_data.append(temp_array)                 df = pd.DataFrame( table_data, columns = column_labels)    axs[i].patch.set_visible(False)    #axs[i].axis('tight')    axs[i].axis('off')    axs[i].table(cellText = df.values, colLabels = df.columns, rowLabels = row_labels, loc="center")    if "PostIrrad" in cwd:     fig.suptitle(r'Halfmoon Diodes Post Irradiation Depletion Voltages $[V]$', fontsize=12)    fig.tight_layout()    plt.subplots_adjust(left=.28, bottom=.02, right=.98, top=.92, wspace=None, hspace=1.5)    plt.savefig('PostIrrad_DepV_Table' + '.png', dpi=1100)    plt.show()        else:    fig.suptitle(r'Halfmoon Diodes Pre Irradiation Depletion Voltages $[V]$', fontsize=10)    fig.tight_layout()    plt.subplots_adjust(left=.3, bottom=.05, right=.98, top=.93, wspace=2, hspace=3.1)    plt.savefig('PreIrrad_DepV_Table' + '.png', dpi=900)    plt.show()#%%# Make Graphs and Dataframe for Each Diodediode_df = make_df(diode_name, diode)# DIODE Graph plt.figure(figsize=(10,8))for i in range(0, num_DIODE):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            diode_df.to_csv('irradiated_diode_data.csv')                else:            factor = scale_factor[1]            diode_df.to_csv('unirradiated_diode_data.csv')                        # Check to make sure sensible values are in the table        if diode[i,j] == 0:            continue                         else:            plt.plot(diode_name[i],-1*diode[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(diode_name[i],-1*diode[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated DIODE', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated DIODE', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('DIODE'+'.png')#%%# Make Dataframe for Printing out .csv laterhalf_df = make_df(half_name, half)half_df.to_csv('irradiated_diodehalf_data.csv')# DIODEHALF Graph   plt.figure(figsize=(10,8)) for i in range(0, num_HALF):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            half_df.to_csv('irradiated_diodehalf_data.csv')                else:            factor = scale_factor[1]            half_df.to_csv('unirradiated_diodehalf_data.csv')                        # Check to make sure sensible values are in the table        if half[i,j] == 0:            continue                         else:            plt.plot(half_name[i],-1*half[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(half_name[i],-1*half[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated DIODEHALF', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated DIODEHALF', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('DIODEHALF'+'.png')#%%# Make Dataframe for Printing out .csv laterpstop_df = make_df(pstop_name, pstop)# DIODEHALFPSTOP Graph plt.figure(figsize=(10,8))for i in range(0, num_PSTOP):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            pstop_df.to_csv('irradiated_diodehalfpstop_data.csv')                else:            factor = scale_factor[1]            pstop_df.to_csv('unirradiated_diodehalfpstop_data.csv')                        # Check to make sure sensible values are in the table        if pstop[i,j] == 0:            continue                         else:            plt.plot(pstop_name[i],-1*pstop[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(pstop_name[i],-1*pstop[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated DIODEHALFPSTOP', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated DIODEHALFPSTOP', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('DIODEHALFPSTOP'+'.png')    #%%# Make Dataframe for Printing out .csv latergr_df = make_df(gr_name, gr)gr_df.to_csv('irradiated_diodehalf_data.csv')# DIODEHALFPSTOP_GR Graph plt.figure(figsize=(10,8))for i in range(0, num_GR):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            gr_df.to_csv('irradiated_diodehalfpstop_gr_data.csv')                else:            factor = scale_factor[1]            gr_df.to_csv('unirradiated_diodehalfpstop_gr_data.csv')                        # Check to make sure sensible values are in the table        if gr[i,j] == 0:            continue                         else:            plt.plot(gr_name[i],-1*gr[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(gr_name[i],-1*gr[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated DIODEHALFPSTOP_GRConnected', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated DIODEHALFPSTOP_GRConnected', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('DIODEHALFPSTOP_GR'+'.png')    #%%# Make Dataframe for Printing out .csv laterquarter_df = make_df(quarter_name, quarter)# DIODEQUARTER Graph plt.figure(figsize=(10,8))for i in range(0, num_QUARTER):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            quarter_df.to_csv('irradiated_diodequarter_data.csv')                else:            factor = scale_factor[1]            quarter_df.to_csv('unirradiated_diodequarter_data.csv')                        # Check to make sure sensible values are in the table        if quarter[i,j] == 0:            continue                         else:            plt.plot(quarter_name[i],-1*quarter[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(quarter_name[i],-1*quarter[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated DIODEQUARTER', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated DIODEQUARTER', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('DIODEQUARTER'+'.png')    #%%    # Make Dataframe for Printing out .csv laterirradsensor_df = make_df(irradsensor_name, irradsensor)    # IRRADSENSOR Graph plt.figure(figsize=(10,8))for i in range(0, num_IRRADSENSOR):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        factor = scale_factor[1]        irradsensor_df.to_csv('unirradiated_irradsensor_data.csv')                        # Check to make sure sensible values are in the table        if irradsensor[i,j] == 0:            continue                         else:            plt.plot(irradsensor_name[i],-1*irradsensor[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(irradsensor_name[i],-1*irradsensor[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated IRRADSENSOR', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated IRRADSENSOR', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('IRRADSENSOR'+'.png')    #%%# Make Dataframe for Printing out .csv laterirradsensor_20min_df = make_df(irradsensor_20min_name, irradsensor_20min)    # IRRADSENSOR 20 Min Graph plt.figure(figsize=(10,8))for i in range(0, num_IRRADSENSOR_20min):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not        if "PostIrrad" in cwd:                factor = scale_factor[0]            irradsensor_20min_df.to_csv('irradiated_irradsensor_20min_data.csv')                        # Check to make sure sensible values are in the table        if irradsensor_20min[i,j] == 0:            continue                         else:            plt.plot(irradsensor_20min_name[i],-1*irradsensor_20min[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(irradsensor_20min_name[i],-1*irradsensor_20min[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        if "PostIrrad" in cwd:                plt.title('Irradiated IRRADSENSOR 20 min', size=15)            plt.ylabel(r'Current $[\mu A]$', size=15)                else:            plt.title('Unirradiated IRRADSENSOR', size=15)             plt.ylabel(r'Current $[nA]$', size=15)                plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('IRRADSENSOR_20min'+'.png')    #%%   # Make Dataframe for Printing out .csv laterirradsensor_1100min_df = make_df(irradsensor_1100min_name, irradsensor_1100min)    # IRRADSENSOR 1100 Min Graph plt.figure(figsize=(10,8))for i in range(0, num_IRRADSENSOR_1100min):       for j in range(0,3):                        # Scale factor depending on whether the diode has been irradiated or not           if "PostIrrad" in cwd:                factor = scale_factor[0]            irradsensor_1100min_df.to_csv('irradiated_irradsensor_1100min_data.csv')                        # Check to make sure sensible values are in the table        if irradsensor_1100min[i,j] == 0:            continue                         else:            plt.plot(irradsensor_1100min_name[i],-1*irradsensor_1100min[i,j]*factor, marker=".", markersize=20, color = current_color[j])                    if i == 0:            plt.plot(irradsensor_1100min_name[i],-1*irradsensor_1100min[i,j]*factor, marker=".", markersize=20, color = current_color[j], label = table_label[j])                    # Scale plots depending on whether diodes have been irradiated or not        plt.title('Irradiated IRRADSENSOR 1100 min', size=15)        plt.ylabel(r'Current $[\mu A]$', size=15)                        plt.legend(loc = 'best')        plt.xticks(rotation=80, size=7)    # Save all the plots corresponding to the same batch to one .png    plt.savefig('IRRADSENSOR_1100min'+'.png')    #%%                                