import fileinput, os, time, xbmc, xbmcgui
try:
	MenuLabel	= sys.argv[1:][0]
except:
	MenuLabel	=  xbmc.getInfoLabel('Container(9000).ListItem.Label2')
try:
	XBE_Edit_Mode	= sys.argv[2:][0]
except:
	XBE_Edit_Mode	= 0
pDialog							= xbmcgui.DialogProgress()
dialog							= xbmcgui.Dialog()
XBE_Files						= 0
EMU_Files						= 0
FAV_Files						= 0
Default_Layout_XML_Path			= "0"
Layout_XML_Path					= "0"
ThemeType						= xbmc.getInfoLabel('Skin.CurrentTheme')
MyPrograms_Path					= xbmc.translatePath('special://skin/xml/MyPrograms.xml')
Custom_Games_Path				= xbmc.translatePath('special://skin/xml/MyPrograms.xml')
_Script_Jump_Path				= xbmc.translatePath('special://skin/xml/_script_jumpList.xml')
FAV_XML_Path					= xbmc.translatePath('special://skin/xml/DialogFavourites.xml')
Favs_List_Path					= xbmc.translatePath('special://xbmc/emustation/gamelists/' + MenuLabel)
Default_Layout_Path				= xbmc.translatePath('special://xbmc/emustation/themes/SIMPLE/layouts/default')
Default_Theme_Layout_Path		= xbmc.translatePath('special://xbmc/emustation/themes/' + ThemeType + '/layouts/default')
Custom_Theme_Layout_Path		= xbmc.translatePath('special://xbmc/emustation/themes/' + ThemeType + '/layouts/' + MenuLabel)
Default_Favs_Layout_Path		= xbmc.translatePath('special://xbmc/emustation/themes/SIMPLE/layouts/favs')
Custom_Theme_Favs_Layout_Path	= xbmc.translatePath('special://xbmc/emustation/themes/' + ThemeType + '/layouts/favs')

Default_Layout					= os.path.join(Default_Theme_Layout_Path, 'layout.xml')
Default_Synopsis_Layout			= os.path.join(Default_Theme_Layout_Path, 'synopsis_layout.xml')
Default_Thumb_Layout			= os.path.join(Default_Theme_Layout_Path, 'thumb_layout.xml')
Default_Video_Layout			= os.path.join(Default_Theme_Layout_Path, 'video_layout.xml')
Default_No_Layout				= os.path.join(Default_Layout_Path, 'layout.xml')
Default_No_Synopsis_Layout		= os.path.join(Default_Layout_Path, 'synopsis_layout.xml')
Default_No_Thumb_Layout			= os.path.join(Default_Layout_Path, 'thumb_layout.xml')
Default_No_Video_Layout			= os.path.join(Default_Layout_Path, 'video_layout.xml')
Custom_Layout					= os.path.join(Custom_Theme_Layout_Path, 'layout.xml')
Custom_Synopsis_Layout			= os.path.join(Custom_Theme_Layout_Path, 'synopsis_layout.xml')
Custom_Thumb_Layout				= os.path.join(Custom_Theme_Layout_Path, 'thumb_layout.xml')
Custom_Video_Layout				= os.path.join(Custom_Theme_Layout_Path, 'video_layout.xml')

Default_Favs_Layout				= os.path.join(Default_Favs_Layout_Path, 'layout.xml')
Default_Favs_Synopsis_Layout	= os.path.join(Default_Favs_Layout_Path, 'synopsis_layout.xml')
Default_Favs_Thumb_Layout		= os.path.join(Default_Favs_Layout_Path, 'thumb_layout.xml')
Default_Favs_Video_Layout		= os.path.join(Default_Favs_Layout_Path, 'video_layout.xml')
Default_No_Favs_Layout			= os.path.join(Default_Favs_Layout_Path, 'layout.xml')
Default_No_Favs_Synopsis_Layout	= os.path.join(Default_Favs_Layout_Path, 'synopsis_layout.xml')
Default_No_Favs_Thumb_Layout	= os.path.join(Default_Favs_Layout_Path, 'thumb_layout.xml')
Default_No_Favs_Video_Layout	= os.path.join(Default_Favs_Layout_Path, 'video_layout.xml')
Custom_Favs_Layout				= os.path.join(Custom_Theme_Favs_Layout_Path, 'layout.xml')
Custom_Favs_Synopsis_Layout		= os.path.join(Custom_Theme_Favs_Layout_Path, 'synopsis_layout.xml')
Custom_Favs_Thumb_Layout		= os.path.join(Custom_Theme_Favs_Layout_Path, 'thumb_layout.xml')
Custom_Favs_Video_Layout		= os.path.join(Custom_Theme_Favs_Layout_Path, 'video_layout.xml')

XBE_Default_Layout				= os.path.join(Default_Theme_Layout_Path, 'XBE files/layout.xml')
XBE_Default_Synopsis_Layout		= os.path.join(Default_Theme_Layout_Path, 'XBE files/synopsis_layout.xml')
XBE_Default_Thumb_Layout		= os.path.join(Default_Theme_Layout_Path, 'XBE files/thumb_layout.xml')
XBE_Default_Video_Layout		= os.path.join(Default_Theme_Layout_Path, 'XBE files/video_layout.xml')
XBE_Default_No_Layout			= os.path.join(Default_Layout_Path, 'XBE files/layout.xml')
XBE_Default_No_Synopsis_Layout	= os.path.join(Default_Layout_Path, 'XBE files/synopsis_layout.xml')
XBE_Default_No_Thumb_Layout		= os.path.join(Default_Layout_Path, 'XBE files/thumb_layout.xml')
XBE_Default_No_Video_Layout		= os.path.join(Default_Layout_Path, 'XBE files/video_layout.xml')


if XBE_Edit_Mode == "editmode" or MenuLabel == "apps" or MenuLabel == "demos":
	XBE_Files = 1
elif MenuLabel == "favs":
	FAV_Files = 1
else:
	EMU_Files = 1

xbmc.executebuiltin('Skin.SetString(emuname,' + MenuLabel + ')')
Header_Data_EMU					= '<window type="window" id="1">\n\
		<onunload condition="Player.HasVideo">Stop</onunload>\n\
		<defaultcontrol always="true">9000</defaultcontrol>\n\
		<allowoverlay>no</allowoverlay>\n\
		<view>50</view>\n\
		<layout>%s</layout>\n\
		<controls>\n\
		<control type="button" id="9200">\n\
			<posx>-500</posx>\n\
		</control>\n\
		<control type="group">\n\
				<visible>!Window.IsVisible(1101)</visible>\n\
				<animation type="Hidden">\n\
						<effect type="fade" start="100" end="0" delay="1100" time="1000"/>\n\
				</animation>\n\
				<include>CommonBackground</include>\n\
		</control>\n\
		<control type="group">\n\
		<include>Layout_Animation</include>\n\
		<animation type="Hidden">\n\
				<effect type="zoom" start="100" end="200" center="auto" easing="in" tween="cubic" delay="100" time="1100"/>\n\
				<effect type="fade" start="100" end="0" delay="300" time="600"/>\n\
		</animation>\n\
		<visible>!Window.IsVisible(1101)</visible>\n\
		<!-- Used to run the script and stop folk moving the list forward or backwards -->\n\
		<control type="button" id="9999">\n\
			<posx>-500</posx>\n\
			<onfocus>RunScript(special://emustation_scripts/play_preview.py)</onfocus>\n\
			<visible>!Skin.HasSetting(videolayout)</visible>\n\
		</control>\n\
		<control type="button" id="9990">\n\
			<posx>-500</posx>\n\
			<onfocus>SetFocus(9000)</onfocus>\n\
			<onfocus>ActivateWindow(1120)</onfocus>\n\
		</control>\n\
		<!-- Used to stop playback if one of the direction buttons are pressed or the (A) button -->\n\
		<control type="button" id="9100">\n\
			<posx>-500</posx>\n\
			<onup>setfocus(9000)</onup>\n\
			<ondown>setfocus(9000)</ondown>\n\
			<onleft>setfocus(9000)</onleft>\n\
			<onright>setfocus(9000)</onright>\n\
			<onclick>setfocus(9000)</onclick>\n\
			<onup>stop</onup>\n\
			<ondown>stop</ondown>\n\
			<onleft>stop</onleft>\n\
			<onright>stop</onright>\n\
			<onclick>stop</onclick>\n\
			<onup>Control.Move(9000,-1)</onup>\n\
			<ondown>Control.Move(9000,1)</ondown>\n\
			<onleft>PageUp</onleft>\n\
			<onright>PageDown</onright>\n\
			<visible>!Skin.HasSetting(videolayout) + !Skin.HasSetting(videopreviewhorizontal)</visible>\n\
		</control>\n\
		<control type="button" id="9100">\n\
			<posx>-500</posx>\n\
			<onup>setfocus(9000)</onup>\n\
			<ondown>setfocus(9000)</ondown>\n\
			<onleft>setfocus(9000)</onleft>\n\
			<onright>setfocus(9000)</onright>\n\
			<onclick>setfocus(9000)</onclick>\n\
			<onup>stop</onup>\n\
			<ondown>stop</ondown>\n\
			<onleft>stop</onleft>\n\
			<onright>stop</onright>\n\
			<onclick>stop</onclick>\n\
			<onup>PageDown</onup>\n\
			<ondown>PageUp</ondown>\n\
			<onleft>Control.Move(9000,-1)</onleft>\n\
			<onright>Control.Move(9000,1)</onright>\n\
			<visible>!Skin.HasSetting(videolayout) + Skin.HasSetting(videopreviewhorizontal)</visible>\n\
		</control>\n\
	'
Footer_Data_EMU					= '\n\
	</control>\n\
	</controls>\n\
	</window>'
Header_Data_FAVS				= '<window type="dialog" id="134">\n\
	<defaultcontrol always="true">450</defaultcontrol>\n\
	<onunload>Skin.Reset(favsloading)</onunload>\n\
	<include>Fav_Layout_Animation</include>\n\
	<controls>\n\
		<control type="button" id="9990">\n\
			<posx>-500</posx>\n\
			<onfocus>SetFocus(1000)</onfocus>\n\
		</control>\n'
Footer_Data_FAVS				= '\n\
	</controls>\n\
	</window>'
if not MenuLabel == "xbox" and not MenuLabel == "ports":
	Jump_File_Data					= '<window type="dialog" id="1120">\n\
		<defaultcontrol always="true">9000</defaultcontrol>\n\
		<controls>\n\
			<control type="group" id="jump section">\n\
				<posy>90</posy>\n\
				<!-- Normal -->\n\
				<control type="group">\n\
					<visible>!Skin.HasSetting(KioskMode) + [!Skin.HasSetting(synopsislayout) | !Skin.HasSetting(videolayout)]</visible>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>165</posx>\n\
						<posy>10</posy>\n\
						<width>950</width>\n\
						<height>530</height>\n\
						<texture>menu_back_shadow.png</texture>\n\
					</control>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>320</posx>\n\
						<posy>100</posy>\n\
						<width>640</width>\n\
						<height>350</height>\n\
						<colordiffuse>menu_back_image</colordiffuse>\n\
						<texture border="20,20,20,20">menu_back.png</texture>\n\
					</control>\n\
				</control>\n\
				<!-- kiosk mode -->\n\
				<control type="group">\n\
					<visible>Skin.HasSetting(KioskMode) + [!Skin.HasSetting(synopsislayout) | !Skin.HasSetting(videolayout)]</visible>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>165</posx>\n\
						<posy>60</posy>\n\
						<width>950</width>\n\
						<height>280</height>\n\
						<texture>menu_back_shadow.png</texture>\n\
					</control>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>320</posx>\n\
						<posy>100</posy>\n\
						<width>640</width>\n\
						<height>200</height>\n\
						<colordiffuse>menu_back_image</colordiffuse>\n\
						<texture border="20,20,20,20">menu_back.png</texture>\n\
					</control>\n\
				</control>\n\
				<control type="label">\n\
					<description>heading label</description>\n\
					<posx>320</posx>\n\
					<posy>130</posy>\n\
					<width>640</width>\n\
					<height>50</height>\n\
					<align>center</align>\n\
					<aligny>center</aligny>\n\
					<font>size_50</font>\n\
					<label>[UPPERCASE]$LOCALIZE[30911][/UPPERCASE]</label>\n\
					<textcolor>menu_header_label</textcolor>\n\
				</control>\n\
				<control type="grouplist" id="9000">\n\
					<posx>320</posx>\n\
					<posy>201</posy>\n\
					<width>640</width>\n\
					<height>50</height>\n\
					<onleft>9000</onleft>\n\
					<onright>9000</onright>\n\
					<onup>9003</onup>\n\
					<ondown>9001</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>horizontal</orientation>\n\
					<!-- jumpcode -->\n\
				</control>\n\
				<control type="grouplist" id="9001">\n\
					<posx>320</posx>\n\
					<posy>250</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>-</onleft>\n\
					<onright>-</onright>\n\
					<onup>9000</onup>\n\
					<ondown>9002</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>vertical</orientation>\n\
					<control type="button" id="8050">\n\
						<label>[UPPERCASE]$LOCALIZE[31400][/UPPERCASE]</label>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onclick>Dialog.Close(1120)</onclick>\n\
						<onclick>SetFocus(9200)</onclick>\n\
						<onclick>RunScript(special://emustation_scripts/generate_favourites.py)</onclick>\n\
						<visible>!Skin.HasSetting(KioskMode)</visible>\n\
					</control>\n\
				</control>\n\
				<control type="grouplist" id="9002">\n\
					<posx>320</posx>\n\
					<posy>299</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>9002</onleft>\n\
					<onright>9002</onright>\n\
					<onup>9001</onup>\n\
					<ondown>9003</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>horizontal</orientation>\n\
					<visible>!Skin.HasSetting(KioskMode)</visible>\n\
					<control type="button" id="8040">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]2d[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,boxart)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),boxart)</visible>\n\
					</control>\n\
					<visible>!StringCompare(Skin.String(emuname),xbox) | !StringCompare(Skin.String(emuname),ports)</visible>\n\
					<control type="button" id="8041">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]3d[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,boxart3d)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),boxart3d)</visible>\n\
					</control>\n\
					<control type="button" id="8042">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]logos[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,logo)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),logo)</visible>\n\
					</control>\n\
					<control type="button" id="8043">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]mix[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,mix)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),mix)</visible>\n\
					</control>\n\
					<control type="button" id="8044">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]screenshots[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,screenshots)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),screenshots)</visible>\n\
					</control>\n\
				</control>\n\
				<control type="grouplist" id="9003">\n\
					<posx>320</posx>\n\
					<posy>348</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>-</onleft>\n\
					<onright>-</onright>\n\
					<onup>9002</onup>\n\
					<ondown>9000</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>vertical</orientation>\n\
					<visible>!Skin.HasSetting(KioskMode) + [Skin.HasSetting(synopsislayout) | Skin.HasSetting(videolayout)]</visible>\n\
					<control type="radiobutton" id="8060">\n\
						<label>[UPPERCASE]$LOCALIZE[31403][/UPPERCASE]</label>\n\
						<include>MenuButtonCommonAltValues</include>\n\
						<onclick>Skin.ToggleSetting(' + MenuLabel + 'fanart)</onclick>\n\
						<selected>Skin.HasSetting(' + MenuLabel + 'fanart)</selected>\n\
					</control>\n\
				</control>\n\
			</control>\n\
		</controls>\n\
	</window>'
else:
	Jump_File_Data					= '<window type="dialog" id="1120">\n\
		<defaultcontrol always="true">9000</defaultcontrol>\n\
		<controls>\n\
			<control type="group" id="jump section">\n\
				<posy>90</posy>\n\
				<animation effect="slide" reversable="true" start="0,0" end="0,-25" time="0" condition="Skin.HasSetting(synopsislayout) + !Skin.HasSetting(KioskMode)">conditional</animation>\n\
				<!-- Normal -->\n\
				<control type="group">\n\
					<visible>!Skin.HasSetting(KioskMode) + [!Skin.HasSetting(synopsislayout) | !Skin.HasSetting(videolayout)]</visible>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>165</posx>\n\
						<posy>10</posy>\n\
						<width>950</width>\n\
						<height>530</height>\n\
						<texture>menu_back_shadow.png</texture>\n\
					</control>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>320</posx>\n\
						<posy>100</posy>\n\
						<width>640</width>\n\
						<height>350</height>\n\
						<colordiffuse>menu_back_image</colordiffuse>\n\
						<texture border="20,20,20,20">menu_back.png</texture>\n\
					</control>\n\
				</control>\n\
				<control type="group">\n\
					<visible>!Skin.HasSetting(KioskMode) + [Skin.HasSetting(synopsislayout) | Skin.HasSetting(videolayout)]</visible>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>165</posx>\n\
						<posy>10</posy>\n\
						<width>950</width>\n\
						<height>580</height>\n\
						<texture>menu_back_shadow.png</texture>\n\
					</control>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>320</posx>\n\
						<posy>100</posy>\n\
						<width>640</width>\n\
						<height>400</height>\n\
						<colordiffuse>menu_back_image</colordiffuse>\n\
						<texture border="20,20,20,20">menu_back.png</texture>\n\
					</control>\n\
				</control>\n\
				<!-- kiosk mode -->\n\
				<control type="group">\n\
					<visible>Skin.HasSetting(KioskMode) + [!Skin.HasSetting(synopsislayout) | !Skin.HasSetting(videolayout)]</visible>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>165</posx>\n\
						<posy>60</posy>\n\
						<width>950</width>\n\
						<height>280</height>\n\
						<texture>menu_back_shadow.png</texture>\n\
					</control>\n\
					<control type="image">\n\
						<description>background image</description>\n\
						<posx>320</posx>\n\
						<posy>100</posy>\n\
						<width>640</width>\n\
						<height>200</height>\n\
						<colordiffuse>menu_back_image</colordiffuse>\n\
						<texture border="20,20,20,20">menu_back.png</texture>\n\
					</control>\n\
				</control>\n\
				<control type="label">\n\
					<description>heading label</description>\n\
					<posx>320</posx>\n\
					<posy>130</posy>\n\
					<width>640</width>\n\
					<height>50</height>\n\
					<align>center</align>\n\
					<aligny>center</aligny>\n\
					<font>size_50</font>\n\
					<label>[UPPERCASE]$LOCALIZE[30911][/UPPERCASE]</label>\n\
					<textcolor>menu_header_label</textcolor>\n\
				</control>\n\
				<control type="grouplist" id="9000">\n\
					<posx>320</posx>\n\
					<posy>201</posy>\n\
					<width>640</width>\n\
					<height>50</height>\n\
					<onleft>9000</onleft>\n\
					<onright>9000</onright>\n\
					<onup>9004</onup>\n\
					<ondown>9001</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>horizontal</orientation>\n\
					<!-- jumpcode -->\n\
				</control>\n\
				<control type="grouplist" id="9001">\n\
					<posx>320</posx>\n\
					<posy>250</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>-</onleft>\n\
					<onright>-</onright>\n\
					<onup>9000</onup>\n\
					<ondown>9002</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>vertical</orientation>\n\
					<control type="button" id="8051">\n\
						<label>[UPPERCASE]$LOCALIZE[31401][/UPPERCASE]</label>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onclick>Dialog.Close(1120)</onclick>\n\
						<onclick>SetFocus(9200)</onclick>\n\
						<onclick>RunScript(special://emustation_scripts/generate_favourites.py)</onclick>\n\
						<visible>!Skin.HasSetting(KioskMode)</visible>\n\
					</control>\n\
				</control>\n\
				<control type="grouplist" id="9002">\n\
					<posx>320</posx>\n\
					<posy>299</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>9002</onleft>\n\
					<onright>9002</onright>\n\
					<onup>9001</onup>\n\
					<ondown>9003</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>horizontal</orientation>\n\
					<visible>!Skin.HasSetting(KioskMode)</visible>\n\
					<control type="button" id="8040">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]2d[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,boxart)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),boxart)</visible>\n\
					</control>\n\
					<control type="button" id="8041">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]3d[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,boxart3d)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),boxart3d)</visible>\n\
					</control>\n\
					<control type="button" id="8042">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]cd poster[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,cdposter)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),cdposter)</visible>\n\
					</control>\n\
					<control type="button" id="8043">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]disc[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,disc)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),disc)</visible>\n\
					</control>\n\
					<control type="button" id="8044">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]dual[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,dual)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),dual)</visible>\n\
					</control>\n\
					<control type="button" id="8045">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]open case[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,opencase)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),opencase)</visible>\n\
					</control>\n\
					<control type="button" id="8046">\n\
						<label>[UPPERCASE]$LOCALIZE[31402][/UPPERCASE]</label>\n\
						<label2>&lt; [UPPERCASE]screenshots[/UPPERCASE] &gt;</label2>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onfocus>Skin.SetString(' + MenuLabel + '_artworkfolder,screenshots)</onfocus>\n\
						<visible allowhiddenfocus="true">StringCompare(Skin.String(' + MenuLabel + '_artworkfolder),screenshots)</visible>\n\
					</control>\n\
				</control>\n\
				<control type="grouplist" id="9003">\n\
					<posx>320</posx>\n\
					<posy>348</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>-</onleft>\n\
					<onright>-</onright>\n\
					<onup>9002</onup>\n\
					<ondown>9004</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>vertical</orientation>\n\
					<visible>!Skin.HasSetting(KioskMode) + [Skin.HasSetting(synopsislayout) | Skin.HasSetting(videolayout)]</visible>\n\
					<control type="radiobutton" id="8060">\n\
						<label>[UPPERCASE]$LOCALIZE[31403][/UPPERCASE]</label>\n\
						<include>MenuButtonCommonAltValues</include>\n\
						<onclick>Skin.ToggleSetting(' + MenuLabel + 'fanart)</onclick>\n\
						<selected>Skin.HasSetting(' + MenuLabel + 'fanart)</selected>\n\
					</control>\n\
				</control>\n\
				<control type="grouplist" id="9004">\n\
					<posx>320</posx>\n\
					<posy>348</posy>\n\
					<width>640</width>\n\
					<height>200</height>\n\
					<onleft>-</onleft>\n\
					<onright>-</onright>\n\
					<onup>9003</onup>\n\
					<ondown>9000</ondown>\n\
					<itemgap>-1</itemgap>\n\
					<scrolltime>0</scrolltime>\n\
					<orientation>vertical</orientation>\n\
					<animation effect="slide" reversable="true" start="0,0" end="0,49" time="0" condition="Skin.HasSetting(synopsislayout) | Skin.HasSetting(videolayout)">conditional</animation>\n\
					<visible>!Skin.HasSetting(KioskMode) + [StringCompare(Skin.String(emuname),xbox) | StringCompare(Skin.String(emuname),ports)]</visible>\n\
					<control type="button" id="8070">\n\
						<label>[UPPERCASE]$LOCALIZE[31404][/UPPERCASE]</label>\n\
						<include>MenuButtonCommonValues</include>\n\
						<onclick>Skin.SetBool(editmode)</onclick>\n\
						<onclick>Dialog.Close(1120)</onclick>\n\
						<onclick>RunScript(special://emustation_scripts/menu_loader.py,'+xbmc.getInfoLabel('Container(9000).ListItem.Label2')+',editmode)</onclick>\n\
					</control>\n\
				</control>\n\
			</control>\n\
		</controls>\n\
	</window>'
Header_Data_XBE					= '<window id="1">\n\
		<onunload condition="Player.HasVideo">Stop</onunload>\n\
		<defaultcontrol always="true">50</defaultcontrol>\n\
		<allowoverlay>no</allowoverlay>\n\
		<view>50</view>\n\
		<layout>%s</layout>\n\
		<controls>\n\
		<include>CommonBackground</include>\n\
		<control type="group">\n\
		<include>Layout_Animation</include>\n\
		<control type="button" id="9990">\n\
			<posx>-500</posx>\n\
			<onfocus>SetFocus(50)</onfocus>\n\
			<onfocus>ContextMenu</onfocus>\n\
		</control>\n\
		<control type="button" id="9000">\n\
			<posx>-500</posx>\n\
			<onfocus>SetFocus(50)</onfocus>\n\
		</control>\n\
		<!-- Used to stop playback if one of the direction buttons are pressed or the (A) button -->\n\
		<control type="button" id="9100">\n\
			<posx>-500</posx>\n\
			<onup>setfocus(50)</onup>\n\
			<ondown>setfocus(50)</ondown>\n\
			<onleft>setfocus(50)</onleft>\n\
			<onright>setfocus(50)</onright>\n\
			<onclick>setfocus(50)</onclick>\n\
			<onup>stop</onup>\n\
			<ondown>stop</ondown>\n\
			<onleft>stop</onleft>\n\
			<onright>stop</onright>\n\
			<onclick>stop</onclick>\n\
			<onup>Control.Move(50,-1)</onup>\n\
			<ondown>Control.Move(50,1)</ondown>\n\
			<onleft>PageUp</onleft>\n\
			<onright>PageDown</onright>\n\
		</control>\n\
	'
Footer_Data_XBE					= '\n\
	</control>\n\
	</controls>\n\
	</window>'
if EMU_Files == 1:
	if xbmc.getCondVisibility('Skin.HasSetting(videolayout)'):
		if os.path.isfile(Custom_Video_Layout):
			Layout_XML_Path			= Custom_Video_Layout
		elif os.path.isfile(Default_Video_Layout):
			Default_Layout_XML_Path	= Default_Video_Layout
		elif os.path.isfile(Default_Synopsis_Layout):
			Default_Layout_XML_Path	= Default_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Video_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(synopsislayout)'):
		if os.path.isfile(Custom_Synopsis_Layout):
			Layout_XML_Path			= Custom_Synopsis_Layout
		elif os.path.isfile(Default_Synopsis_Layout):
			Default_Layout_XML_Path	= Default_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Synopsis_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(thumblayout)'):
		if os.path.isfile(Custom_Thumb_Layout):
			Layout_XML_Path			= Custom_Thumb_Layout
		elif os.path.isfile(Default_Thumb_Layout):
			Default_Layout_XML_Path	= Default_Thumb_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Thumb_Layout
	else:
		if os.path.isfile(Custom_Layout):
			Layout_XML_Path				= Custom_Layout
		elif os.path.isfile(Default_Layout):
			Default_Layout_XML_Path		= Default_Layout
		else:
			Default_Layout_XML_Path		= Default_No_Layout
elif FAV_Files == 1:
	if xbmc.getCondVisibility('Skin.HasSetting(videolayout)'):
		if os.path.isfile(Custom_Favs_Video_Layout):
			Layout_XML_Path			= Custom_Video_Layout
		elif os.path.isfile(Default_Favs_Video_Layout):
			Default_Layout_XML_Path	= Default_Favs_Video_Layout
		elif os.path.isfile(Default_Favs_Synopsis_Layout):
			Default_Layout_XML_Path	= Default_Favs_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Favs_Video_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(synopsislayout)'):
		if os.path.isfile(Custom_Favs_Synopsis_Layout):
			Layout_XML_Path			= Custom_Favs_Synopsis_Layout
		elif os.path.isfile(Default_Favs_Synopsis_Layout):
			Default_Layout_XML_Path	= Default_Favs_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Favs_Synopsis_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(thumblayout)'):
		if os.path.isfile(Custom_Favs_Thumb_Layout):
			Layout_XML_Path			= Custom_Favs_Thumb_Layout
		elif os.path.isfile(Default_Favs_Thumb_Layout):
			Default_Layout_XML_Path	= Default_Favs_Thumb_Layout
		else:
			Default_Layout_XML_Path	= Default_No_Favs_Thumb_Layout
	else:
		if os.path.isfile(Custom_Favs_Layout):
			Layout_XML_Path				= Custom_Favs_Layout
		elif os.path.isfile(Default_Favs_Layout):
			Default_Layout_XML_Path		= Default_Favs_Layout
		else:
			Default_Layout_XML_Path		= Default_No_Favs_Layout
elif XBE_Files == 1:
	if xbmc.getCondVisibility('Skin.HasSetting(videolayout)'):
		if os.path.isfile(XBE_Default_Video_Layout):
			Default_Layout_XML_Path	= XBE_Default_Video_Layout
		elif os.path.isfile(XBE_Default_Synopsis_Layout):
			Default_Layout_XML_Path	= XBE_Default_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= XBE_Default_No_Video_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(synopsislayout)'):
		if os.path.isfile(XBE_Default_Synopsis_Layout):
			Default_Layout_XML_Path	= XBE_Default_Synopsis_Layout
		else:
			Default_Layout_XML_Path	= XBE_Default_No_Synopsis_Layout
	elif xbmc.getCondVisibility('Skin.HasSetting(thumblayout)'):
		if os.path.isfile(XBE_Default_Thumb_Layout):
			Default_Layout_XML_Path	= XBE_Default_Thumb_Layout
		else:
			Default_Layout_XML_Path	= XBE_Default_No_Thumb_Layout
	else:
		if os.path.isfile(XBE_Default_Layout):
			Default_Layout_XML_Path		= XBE_Default_Layout
		else:
			Default_Layout_XML_Path		= XBE_Default_No_Layout
if os.path.isfile(Layout_XML_Path):
	Layout_File =  Layout_XML_Path
elif os.path.isfile(Default_Layout_XML_Path):
	Layout_File =  Default_Layout_XML_Path
else:	# default layout is missing so error!
	EMU_Files = 0; FAV_Files = 0; XBE_Files = 0;
	xbmc.executebuiltin('SetFocus(9000)')
	dialog.ok("ERROR","Default layout file is missing.",Default_Layout_XML_Path)
if EMU_Files == 1:
	if os.path.isfile(os.path.join(Favs_List_Path,'gamelist.xml')):
		## this is here so not to mess with the actual menulabel
		if not os.path.isfile(Layout_XML_Path):
			MenuLabel_XML = "default"
		else:
			MenuLabel_XML = MenuLabel
		Header_Data = Header_Data_EMU % (MenuLabel_XML)
		try:
			with open(Layout_File) as layoutfile:
				with open(Custom_Games_Path, "w") as inputfile:
					inputfile.write(Header_Data)
					for code in layoutfile:
						code = code.replace('[ArtworkFolder]',xbmc.getInfoLabel('skin.string(Custom_Media_Path)') + xbmc.getInfoLabel('Skin.String(emuname)') + '\$INFO[Skin.String('+ MenuLabel +'_artworkfolder)]\\')
						code = code.replace('[Fanart_Toggle]','Skin.HasSetting(' + xbmc.getInfoLabel('Skin.String(emuname)') + 'fanart)')
						code = code.replace('[Media_Path]',xbmc.getInfoLabel('skin.string(Custom_Media_Path)') + xbmc.getInfoLabel('Skin.String(emuname)'))
						code = code.replace('[CurrentSystem]',MenuLabel)
						if '<!-- video preview mode horizontal -->' in code: xbmc.executebuiltin('Skin.SetBool(videopreviewhorizontal)')
						inputfile.write(code)
					inputfile.write(Footer_Data_EMU)
			with open(os.path.join(Favs_List_Path,'gamelist.xml')) as gamelistfile:
				gamelistfile = gamelistfile.read()
				gamelistfile = gamelistfile.replace('[ArtworkFolder]',xbmc.getInfoLabel('skin.string(Custom_Media_Path)') + xbmc.getInfoLabel('Skin.String(emuname)') + '\$INFO[Skin.String('+ MenuLabel +'_artworkfolder)]\\')
				for line in fileinput.FileInput(Custom_Games_Path,inplace=1):
					if '<!-- content list this label is required -->' in line:
						line = line.replace(line,line+gamelistfile)
					print line,
			with open(_Script_Jump_Path, "w") as inputfile:
				inputfile.write(Jump_File_Data)
			with open(os.path.join(Favs_List_Path,'jumplist.xml')) as jumpfile:
				jumpfile = jumpfile.read()
				for line in fileinput.FileInput(_Script_Jump_Path,inplace=1):
					if '<!-- jumpcode -->' in line:
						line = line.replace(line,line+jumpfile)
					print line,
		except:
			pass
		time.sleep(0.5) # delay to make sure the file is written
		if xbmc.getCondVisibility('Skin.HasSetting(videolayout)'):
			xbmc.executebuiltin('RunScript(special://emustation_scripts/auto_play_preview.py)')
		else:
			xbmc.executebuiltin('ActivateWindow(Programs,Static_Menu,return)')
	else:	# default layout is missing so error!
		xbmc.executebuiltin('SetFocus(9000)')
		if MenuLabel == "xbox":
			dialog.ok("ERROR","No game list found","Rescan your xbox games to fix.",os.path.join(Favs_List_Path,'gamelist.xml'))
		elif MenuLabel == "ports":
			dialog.ok("ERROR","No game list found","Rescan your xbox ports to fix.",os.path.join(Favs_List_Path,'gamelist.xml'))
		else:
			dialog.ok("ERROR","No rom list found","Rescan this emulator for roms to fix.",os.path.join(Favs_List_Path,'gamelist.xml'))
elif XBE_Files == 1:
		## this is here so not to mess with the actual menulabel
		if not os.path.isfile(Layout_XML_Path):
			MenuLabel_XML = "default"
		else:
			MenuLabel_XML = MenuLabel
		Header_Data = Header_Data_XBE % (MenuLabel_XML)
		try:
			with open(Layout_File) as layoutfile:
				with open(MyPrograms_Path, "w") as inputfile:
					inputfile.write(Header_Data)		
					for code in layoutfile:
						inputfile.write(code)
					inputfile.write(Footer_Data_XBE)
		except:
			pass
		time.sleep(0.5) # delay to make sure the file is written
		xbmc.executebuiltin('Dialog.Close(1111,true)')
		xbmc.executebuiltin('ActivateWindow(Programs,'+ MenuLabel +',return)')
elif FAV_Files == 1:
		try:
			with open(Layout_File) as layoutfile:
				with open(FAV_XML_Path, "w") as inputfile:
					inputfile.write(Header_Data_FAVS)
					for code in layoutfile:
						inputfile.write(code)
					inputfile.write(Footer_Data_FAVS)
		except:
			pass
		xbmc.executebuiltin('Skin.SetBool(favsloading)')
		time.sleep(0.5) # delay to make it seem like it loading the menu
		xbmc.executebuiltin('ReplaceWindow(134,return)')
else:
	xbmc.executebuiltin('SetFocus(9000)')
xbmc.executebuiltin('Dialog.Close(1101,true)')