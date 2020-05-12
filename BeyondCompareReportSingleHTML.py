import os
import re
import base64
import glob
 
class BeyondCompareReportSingleHTML(object):
    def __init__(self, report_path):
        self.report_path = report_path
        self.img_folder = 'BcImages'
        self.img_type = 'png'
        self.css_prefix = 'data:image/png;base64,'
        
        with open(self.report_path, 'r', encoding='utf-8') as text:
            self.report_html = text.read()
        self.report_output = self.report_html


    def imgBase64CSS(self):
        self.imgDict = {}
        for img in glob.glob(os.path.join(
                os.path.dirname(self.report_path),
                self.img_folder,
                f'*.{self.img_type}')):
            with open(img, 'rb') as img_file:
                self.imgDict[img.split('\\')[-1].replace(f'.{self.img_type}', '')] = self.css_prefix + base64.b64encode(img_file.read()).decode("utf-8")
        
        self.css_text = '\n'.join([f'img.{k} {{ float:left; content:url({v}) }}' for k,v in self.imgDict.items()])
        
        self.report_output = self.report_output.replace('</style>', self.css_text + '\n</style>')
        self.report_output = self.report_output.replace(f'<img src="{self.img_folder}/', '<img class="')
        self.report_output = self.report_output.replace(f'.{self.img_type}" alt=', '" alt=')

        return

    def commentColumn(self):
        self.report_output = self.report_output.replace(
            '</tr>',
            '<td class="DirItemOlder AlignLeft"></td>\n</tr>')
        self.report_output = self.report_output.replace(
            '<td class="DirItemHeader">Modified</td>\n<td class="DirItemOlder AlignLeft"></td>',
            '<td class="DirItemHeader">Modified</td>\n<td class="DirItemHeader">Comment</td>\n</tr>')
        self.report_output = self.report_output.replace(
            '<td class="DirItemHeader">修改 (M)</td>\n<td class="DirItemOlder AlignLeft"></td>',
            '<td class="DirItemHeader">修改 (M)</td>\n<td class="DirItemHeader">Comment</td>\n</tr>')
        
        return

    def singleHTML(self, report_path_new):
        self.report_path_new = report_path_new
        
        self.imgBase64CSS()
        self.commentColumn()
        
        with open(self.report_path_new, 'w', encoding='utf-8') as output:
            output.write(self.report_output)
        return

if __name__ == '__main__':
    bc = BeyondCompareReportSingleHTML('Report.html')
    bc.singleHTML('Report_new.html')
