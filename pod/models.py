from django.db import models

class Scrappeddata(models.Model):
    url = models.URLField(max_length=1000)
    title = models.CharField(max_length=400, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.url


    # @property
    # def content_blocks(self):
    #     """Parse the content string into blocks for template display"""
    #     try:
    #         # Split content by double newlines (assuming this format from the scraper)
    #         blocks = self.content.split('\n\n')
    #         parsed_blocks = []
            
    #         for block in blocks:
    #             if not block.strip():
    #                 continue
                    
    #             block_data = {}
    #             lines = block.split('\n')
                
    #             for line in lines:
    #                 if line.startswith('Headline: '):
    #                     block_data['headline'] = line[10:]
    #                 elif line.startswith('Span: '):
    #                     block_data['span'] = line[6:]
    #                 elif line.startswith('Paragraph: '):
    #                     block_data['paragraph'] = line[11:]
                
    #             if block_data:
    #                 parsed_blocks.append(block_data)
                    
    #         return parsed_blocks
    #     except Exception:
    #         return []