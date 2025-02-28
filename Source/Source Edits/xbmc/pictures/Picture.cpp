/*
 *      Copyright (C) 2005-2013 Team XBMC
 *      http://xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

#include "pictures/Picture.h"
#include "TextureManager.h"
#include "settings/AdvancedSettings.h"
#include "settings/GUISettings.h"
#include "FileItem.h"
#include "FileSystem/File.h"
#include "FileSystem/CurlFile.h"
#include "DDSImage.h"
#include "JPEGIO.h"
#include "utils/URIUtils.h"
#include "utils/Crc32.h"
#include <XGraphics.h>
#include "d3dx8.h"
#include "XBTF.h"
#include "utils/log.h"

using namespace XFILE;

CPicture::CPicture(void)
{
  ZeroMemory(&m_info, sizeof(ImageInfo));
}

CPicture::~CPicture(void)
{

}

IDirect3DTexture8* CPicture::Load(const CStdString& file, int width, int height)
{
  /*
    DDS files are not yet generated by xbmc. This setting simply enables support required
    to render them properly. They must be created offline currently. We are currently only 
    supporting DXT1 format with no mipmaps that are generated by a utility that marks them
    correctly for use by xbmc. These DDS files are pre-padded to POT to simplify/speedup
    handling.
  */
  if (g_advancedSettings.m_useddsfanart)
  {
    //If a .dds version of the image exists we load it instead.
    CStdString ddsPath = URIUtils::ReplaceExtension(file, ".dds");
    if (CFile::Exists(ddsPath))
    {
      CDDSImage img;
      if (img.ReadFile(ddsPath))
      {
        memset(&m_info, 0, sizeof(ImageInfo));
        /*
          GetOrgWidth() and GetOrgHeight() return the actual size of the image stored in the dds file,
          as opposed to the texture size (which is always POT)
        */
        m_info.originalwidth = m_info.width = img.GetOrgWidth();
        m_info.originalheight = m_info.height = img.GetOrgHeight();
        LPDIRECT3DTEXTURE8 pTexture = NULL;
        //Texture is created using GetWidth and GetHeight, which return texture size (always POT)
        g_graphicsContext.Get3DDevice()->CreateTexture(img.GetWidth(), img.GetHeight(), 1, 0, D3DFMT_DXT1 , D3DPOOL_MANAGED, &pTexture);
        if (pTexture)
        {
          D3DLOCKED_RECT lr;
          if ( D3D_OK == pTexture->LockRect( 0, &lr, NULL, 0 ))
          {
            BYTE *pixels = (BYTE *)lr.pBits;
            //DDS Textures are always POT and don't need decoding, just memcpy into the texture.
            memcpy(pixels, img.GetData(), img.GetSize());
            pTexture->UnlockRect( 0 );
          }
          return pTexture;
        }
        else
        {
          CLog::Log(LOGERROR, "%s - failed to create texture from dds image %s", __FUNCTION__, ddsPath.c_str());
          //fall through to default image loading code
        }
      }
      else
      {
        CLog::Log(LOGERROR, "%s - could not read dds image %s", __FUNCTION__, ddsPath.c_str());
        //fall through to default image loading code
      }
    }
  }

   MEMORYSTATUS stat;
   GlobalMemoryStatus(&stat);
   DWORD dwMegFree = (DWORD)(stat.dwAvailPhys / (1024 * 1024));
  if (dwMegFree >= 8)
  {
	//ImageLib is sooo sloow for jpegs. Try our own decoder first. If it fails, fall back to ImageLib.
	  if (URIUtils::GetExtension(file).Equals(".jpg") || URIUtils::GetExtension(file).Equals(".tbn"))
	  {
		CJpegIO jpegImage;
		if (jpegImage.Open(file, width, height))
		{
		  if (jpegImage.OrgWidth() == 0 || jpegImage.OrgHeight() == 0)
			return NULL;

		  memset(&m_info, 0, sizeof(ImageInfo));
		  m_info.originalwidth = jpegImage.OrgWidth();
		  m_info.originalheight = jpegImage.OrgHeight();
		  m_info.width = jpegImage.Width();
		  m_info.height = jpegImage.Height();
		  LPDIRECT3DTEXTURE8 pTexture = NULL;
		  g_graphicsContext.Get3DDevice()->CreateTexture(((m_info.width + 3) / 4) * 4, ((m_info.height + 3) / 4) * 4, 1, 0, D3DFMT_LIN_A8R8G8B8 , D3DPOOL_MANAGED, &pTexture);
		  if (pTexture)
		  {
			D3DLOCKED_RECT lr;
			if ( D3D_OK == pTexture->LockRect( 0, &lr, NULL, 0 ))
			{
			  DWORD destPitch = lr.Pitch;
			  BYTE *pixels = (BYTE *)lr.pBits;
			  bool ret = jpegImage.Decode(pixels, destPitch, XB_FMT_A8R8G8B8);
			  pTexture->UnlockRect( 0 );
			  if (ret)
				return pTexture;
			  else
				return NULL;
			}
		  }
		  else {
			CLog::Log(LOGERROR, "%s - failed to create texture while loading image using JpegIO %s", __FUNCTION__, file.c_str());
			return NULL;
		  }
		}
	  }
  }
  DllImageLib dll;
  if (!dll.Load()) return NULL;

  memset(&m_info, 0, sizeof(ImageInfo));
  if (!dll.LoadImage(file.c_str(), width, height, &m_info))
  {
    CLog::Log(LOGERROR, "PICTURE: Error loading image %s", file.c_str());
    return NULL;
  }
  LPDIRECT3DTEXTURE8 pTexture = NULL;
  g_graphicsContext.Get3DDevice()->CreateTexture(m_info.width, m_info.height, 1, 0, D3DFMT_LIN_A8R8G8B8 , D3DPOOL_MANAGED, &pTexture);
  if (pTexture)
  {
    D3DLOCKED_RECT lr;
    if ( D3D_OK == pTexture->LockRect( 0, &lr, NULL, 0 ))
    {
      DWORD destPitch = lr.Pitch;
      // CxImage aligns rows to 4 byte boundaries
      DWORD srcPitch = ((m_info.width + 1)* 3 / 4) * 4;
      BYTE *pixels = (BYTE *)lr.pBits;
      for (unsigned int y = 0; y < m_info.height; y++)
      {
        BYTE *dst = pixels + y * destPitch;
        BYTE *src = m_info.texture + (m_info.height - 1 - y) * srcPitch;
        BYTE *alpha = m_info.alpha + (m_info.height - 1 - y) * m_info.width;
        for (unsigned int x = 0; x < m_info.width; x++)
        {
          *dst++ = *src++;
          *dst++ = *src++;
          *dst++ = *src++;
          *dst++ = (m_info.alpha) ? *alpha++ : 0xff;  // alpha
        }
      }
      pTexture->UnlockRect( 0 );
    }
  }
  else
    CLog::Log(LOGERROR, "%s - failed to create texture while loading image using ImageLib %s", __FUNCTION__, file.c_str());
  dll.ReleaseImage(&m_info);
  return pTexture;

}

bool CPicture::CreateThumbnail(const CStdString& file, const CStdString& thumbFile, bool checkExistence /*= false*/)
{
  // don't create the thumb if it already exists
  if (checkExistence && CFile::Exists(thumbFile))
    return true;

  return CacheImage(file, thumbFile, g_advancedSettings.m_thumbSize, g_advancedSettings.m_thumbSize);
}

bool CPicture::CacheImage(const CStdString& sourceUrl, const CStdString& destFile, int width, int height)
{
  if (width > 0 && height > 0)
  {
    CLog::Log(LOGINFO, "Caching image from: %s to %s with width %i and height %i", sourceUrl.c_str(), destFile.c_str(), width, height);

    CJpegIO jpegImage;
    DllImageLib dll;
    bool ret;

    CStdString tempFile(sourceUrl);
    bool isTemp(false);
    if (URIUtils::IsInternetStream(sourceUrl, true))
    {
      Crc32 crc;
      crc.ComputeFromLowerCase(sourceUrl);
      tempFile.Format("special://temp/%08x%s", (unsigned __int32)crc, URIUtils::GetExtension(sourceUrl).c_str());
      CCurlFile stream;
      if (!stream.Download(sourceUrl, tempFile))
        return false;
      isTemp = true;
    }

    ret = false;
    if (URIUtils::GetExtension(sourceUrl).Equals(".jpg") || URIUtils::GetExtension(sourceUrl).Equals(".tbn"))
      ret = jpegImage.CreateThumbnail(tempFile, destFile, width, height);

    if (!ret)
    {
      if (!dll.Load()) return false;
      if (!dll.CreateThumbnail(tempFile.c_str(), destFile.c_str(), width, height, g_guiSettings.GetBool("pictures.useexifrotation")))
      {
        CLog::Log(LOGERROR, "%s Unable to create new image %s from image %s", __FUNCTION__, destFile.c_str(), sourceUrl.c_str());
        return false;
      }
    }
    if (isTemp)
      CFile::Delete(tempFile);
  }
  else
  {
    CLog::Log(LOGINFO, "Caching image from: %s to %s", sourceUrl.c_str(), destFile.c_str());
    if (URIUtils::IsInternetStream(sourceUrl, true))
    {
      CCurlFile stream;
      return stream.Download(sourceUrl, destFile);
    }
    else
      return CFile::Cache(sourceUrl, destFile);
  }
  return true;
}

bool CPicture::CacheThumb(const CStdString& sourceUrl, const CStdString& destFile)
{
  return CacheImage(sourceUrl, destFile, g_advancedSettings.m_thumbSize, g_advancedSettings.m_thumbSize);
}

bool CPicture::CacheFanart(const CStdString& sourceUrl, const CStdString& destFile)
{
  int height = g_advancedSettings.m_fanartHeight;
  // Assume 16:9 size
  int width = height * 16 / 9;

  return CacheImage(sourceUrl, destFile, width, height);
}

bool CPicture::CreateThumbnailFromMemory(const unsigned char* buffer, int bufSize, const CStdString& extension, const CStdString& thumbFile)
{
  CLog::Log(LOGINFO, "Creating album thumb from memory: %s", thumbFile.c_str());
  if (extension.Equals("jpg") || extension.Equals("tbn"))
  {
    CJpegIO jpegImage;
    if (jpegImage.CreateThumbnailFromMemory((unsigned char*)buffer, bufSize, thumbFile.c_str(), g_advancedSettings.m_thumbSize, g_advancedSettings.m_thumbSize))
      return true;
  }
  DllImageLib dll;
  if (!dll.Load()) return false;
  if (!dll.CreateThumbnailFromMemory((BYTE *)buffer, bufSize, extension.c_str(), thumbFile.c_str(), g_advancedSettings.m_thumbSize, g_advancedSettings.m_thumbSize))
  {
    CLog::Log(LOGERROR, "%s: exception with fileType: %s", __FUNCTION__, extension.c_str());
    return false;
  }
  return true;
}

void CPicture::CreateFolderThumb(const CStdString *thumbs, const CStdString &folderThumb)
{ // we want to mold the thumbs together into one single one
  DllImageLib dll;
  if (!dll.Load()) return;
  CStdString cachedThumbs[4];
  const char *szThumbs[4];
  for (int i=0; i < 4; i++)
  {
    if (!thumbs[i].IsEmpty())
    {
      CFileItem item(thumbs[i], false);
      cachedThumbs[i] = item.GetCachedPictureThumb();
      CreateThumbnail(thumbs[i], cachedThumbs[i], true);
    }
    szThumbs[i] = cachedThumbs[i].c_str();
  }
  if (!dll.CreateFolderThumbnail(szThumbs, folderThumb.c_str(), g_advancedSettings.m_thumbSize, g_advancedSettings.m_thumbSize))
  {
    CLog::Log(LOGERROR, "%s failed for folder thumb %s", __FUNCTION__, folderThumb.c_str());
  }
}

bool CPicture::CreateThumbnailFromSurface(const unsigned char *buffer, int width, int height, int stride, const CStdString &thumbFile)
{
  if (URIUtils::GetExtension(thumbFile).Equals(".jpg"))
  {
    CJpegIO jpegImage;
    if (jpegImage.CreateThumbnailFromSurface((BYTE *)buffer, width, height, XB_FMT_A8R8G8B8, stride, thumbFile.c_str()))
      return true;
  }
  DllImageLib dll;
  if (!buffer || !dll.Load()) return false;
  return dll.CreateThumbnailFromSurface((BYTE *)buffer, width, height, stride, thumbFile.c_str());
}

int CPicture::ConvertFile(const CStdString &srcFile, const CStdString &destFile, float rotateDegrees, int width, int height, unsigned int quality, bool mirror)
{
  DllImageLib dll;
  if (!dll.Load()) return false;
  int ret = dll.ConvertFile(srcFile.c_str(), destFile.c_str(), rotateDegrees, width, height, quality, mirror);
  if (ret)
  {
    CLog::Log(LOGERROR, "PICTURE: Error %i converting image %s", ret, srcFile.c_str());
    return ret;
  }
  return ret;
}

// caches a skin image as a thumbnail image
bool CPicture::CacheSkinImage(const CStdString &srcFile, const CStdString &destFile)
{
  int iImages = g_TextureManager.Load(srcFile);
  if (iImages > 0)
  {
    CTexture texture = g_TextureManager.GetTexture(srcFile);
    if (texture.size())
    {
      bool success(false);
      CPicture pic;
      if (!texture.m_texCoordsArePixels)
      { // damn, have to copy it to a linear texture first :(
        return CreateThumbnailFromSwizzledTexture(texture.m_textures[0], texture.m_width, texture.m_height, destFile);
      }
      else
      {
        D3DLOCKED_RECT lr;
        texture.m_textures[0]->LockRect(0, &lr, NULL, 0);
        success = pic.CreateThumbnailFromSurface((BYTE *)lr.pBits, texture.m_width, texture.m_height, lr.Pitch, destFile);
        texture.m_textures[0]->UnlockRect(0);
      }
      g_TextureManager.ReleaseTexture(srcFile);
      return success;
    }
  }
  return false;
}

bool CPicture::CreateThumbnailFromSwizzledTexture(LPDIRECT3DTEXTURE8 &texture, int width, int height, const CStdString &thumbFile)
{
  LPDIRECT3DTEXTURE8 linTexture = NULL;
  if (D3D_OK == D3DXCreateTexture(g_graphicsContext.Get3DDevice(), width, height, 1, 0, D3DFMT_LIN_A8R8G8B8, D3DPOOL_MANAGED, &linTexture))
  {
    LPDIRECT3DSURFACE8 source;
    LPDIRECT3DSURFACE8 dest;
    texture->GetSurfaceLevel(0, &source);
    linTexture->GetSurfaceLevel(0, &dest);
    D3DXLoadSurfaceFromSurface(dest, NULL, NULL, source, NULL, NULL, D3DX_FILTER_NONE, 0);
    D3DLOCKED_RECT lr;
    dest->LockRect(&lr, NULL, 0);
    bool success = CreateThumbnailFromSurface((BYTE *)lr.pBits, width, height, lr.Pitch, thumbFile);
    dest->UnlockRect();
    SAFE_RELEASE(source);
    SAFE_RELEASE(dest);
    SAFE_RELEASE(linTexture);
    return success;
  }
  return false;
}

