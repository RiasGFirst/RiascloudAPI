from bs4 import BeautifulSoup

def main():

    html = '''<div class="_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _1Qs6zz6oqdrQbR7yE_ntfY Post t3_14am3sh" data-adclicklocation="background" data-testid="post-container" id="t3_14am3sh" tabindex="-1"><div></div><div class="_23h0-EcaBUorIHC-JZyh6J" style="width:40px;border-left:4px solid transparent"><div class="_1E9mcoVn4MYnuBQSVDt1gC" id="vote-arrows-t3_14am3sh"><button aria-label="Upvote" aria-pressed="false" class="voteButton" data-adclicklocation="upvote" data-click-id="upvote" id="upvote-button-t3_14am3sh"><span class="_2q7IQ0BUOWeEZoeAxN555e _3SUsITjKNQ7Tp0Wi2jGxIM qW0l8Af61EP35WIG6vnGk _3edNsMs0PNfyQYofMNVhsG"><i class="icon icon-upvote _2Jxk822qXs4DaXwsN7yyHA"></i></span></button><div class="_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo" style="color:#D7DADC"><span></span><span id="vote_t3_14am3sh_count_anim"></span>71</div><button aria-label="Downvote" aria-pressed="false" class="voteButton" data-adclicklocation="downvote" data-click-id="downvote"><span class="_1iKd82bq_nqObFvSH1iC_Q Q0BxYHtCOJ_rNSPJMU2Y7 _2fe-KdD2OM0ciaiux-G1EL _3yQIOwaIuF6gn8db96Gu7y"><i class="icon icon-downvote ZyxIIl4FP5gHGrJDzNpUC"></i></span></button></div></div><div class="_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3 _1Qs6zz6oqdrQbR7yE_ntfY" data-adclicklocation="background" data-click-id="background" style="background:#1A1A1B"><div class="_14-YvdFiW5iVvfe5wdgmET"><div class="cZPZhMe-UCZ8htPodMyJ5"><div class="_3AStxql1mQsrZuUIFP9xSg nU4Je7n-eSXStTBAPMYt8" data-adclicklocation="top_bar"><span class="_2fCzxBE1dlMh4OFc7B3Dun" style="color:#818384">publiée par</span> <div class="_2mHuuvyV9doV3zwbZPtIPG"><div id="UserInfoTooltip--t3_14am3sh"><a class="_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE" data-click-id="user" data-testid="post_author_link" href="/user/pandaredss/" style="color: rgb(129, 131, 132);">u/pandaredss</a></div></div><span class="_2VF2J19pUIMSLJFky-7PEI" data-click-id="timestamp" data-testid="post_timestamp" style="color:#818384">il y a 7 heures</span></div><div class="_2wFk1qX4e1cxk8Pkw1rAHk"></div><div class="_3XoW0oYd5806XiOr24gGdb"></div></div></div><div class="_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 t3_14am3sh" data-adclicklocation="title"><div class="_2xu1HuBz1Yx6SP10AGVx_I" data-ignore-click="false"><div class="lrzZ8b0L6AzLkQj5Ww7H1"></div><div class="lrzZ8b0L6AzLkQj5Ww7H1"><a href="/r/cosplay/?f=flair_name%3A%22Self%22"><span class="_1jNPl3YUk6zbpLWdjaJT1r _2VqfzH0dZ9dIl3XWNxs42y aJrgrewN9C8x1Fusdx4hh _1Dl-kvSxyJMWO9nuoTof8N" style="background-color:#94e044;color:#000000">Self</span></a></div></div><div class="y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE"><a class="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE" data-click-id="body" href="/r/cosplay/comments/14am3sh/viking_cosplay_by_akari/"><div class="_2SdHzo12ISmrC8H86TgSCp _3wqmjmv3tb_k-PROt7qFZe" style="--posttitletextcolor:#D7DADC"><h3 class="_eYtD2XCVieq6emjKBH3m">Viking cosplay by Akari</h3></div></a></div><div class="_1hLrLjnE1G_RBCNcN9MVQf">
<img alt="" onload="(__markFirstPostVisible || function(){})();" src="https://www.redditstatic.com/desktop2x/img/renderTimingPixel.png" style="width: 1px; height: 1px;"/>
</div><style>
        .t3_14am3sh._2FCtq-QzlfuN-SwVMUZMM3 {
          --postTitle-VisitedLinkColor: #edeeef;
          --postTitleLink-VisitedLinkColor: #6f7071;
          --postBodyLink-VisitedLinkColor: #6f7071;
        }
      </style></div><div class="STit0dLageRsa2yR4te_b"><div class="m3aNC6yp8RrNM_-a0rrfa _3PIKVMCKdveCEcyiKr43sU" data-click-id="media" style="max-height:488.8125px"><div class="_3gBRFDB5C34UWyxEe_U6mD" style="padding-bottom:56.25%"></div><div class="_3JgI-GOrkmyIeDeyzXdyUD _2CSlKHjH7lsjx0IpjORx14"><div data-testid="shreddit-player-wrapper" style="background-color: black; color: white; cursor: default; height: 100%; margin: 0px auto; max-height: 100%; max-width: 100%; width: 100%;"><media-telemetry-observer><shreddit-player autoplay="" autoplay-pref="true" poster="https://external-preview.redd.it/X1SsNcCXUeHFMm4geUwcpNvCmLpHY8jZ9iJXHZmPfJA.png?width=960&amp;crop=smart&amp;format=pjpg&amp;auto=webp&amp;v=enabled&amp;s=7fb52fe1b14738da35f4535ac9e3daeb6f9952bd" preview="https://v.redd.it/z17515gwwa6b1/DASH_96.mp4" show-autoplay-toggle="true" src="https://v.redd.it/z17515gwwa6b1/HLSPlaylist.m3u8?a=1689505878%2CNzM5ZGUwYTE4ZWYyMWRjYTc2MzgxNDc4NzYyY2IyOGRjYWZmMWIxNTgyOTNkMjRiOGI4NDJkNmUzYzQ3NGQzMw%3D%3D&amp;v=1&amp;f=sd" ui="desktop"><source src="https://v.redd.it/z17515gwwa6b1/HLSPlaylist.m3u8?a=1689505878%2CNzM5ZGUwYTE4ZWYyMWRjYTc2MzgxNDc4NzYyY2IyOGRjYWZmMWIxNTgyOTNkMjRiOGI4NDJkNmUzYzQ3NGQzMw%3D%3D&amp;v=1&amp;f=sd" type="application/vnd.apple.mpegURL"/></shreddit-player></media-telemetry-observer></div></div></div></div><div class="_1ixsU4oQRnNfZ91jhBU74y"><div class="_1E9mcoVn4MYnuBQSVDt1gC _2oM1YqCxIwkvwyeZamWwhW uFwpR-OdmueYZxdY_rEDX" id="vote-arrows-t3_14am3sh"><button aria-label="Upvote" aria-pressed="false" class="voteButton" data-adclicklocation="upvote" data-click-id="upvote"><span class="_2q7IQ0BUOWeEZoeAxN555e _3SUsITjKNQ7Tp0Wi2jGxIM qW0l8Af61EP35WIG6vnGk _3edNsMs0PNfyQYofMNVhsG"><i class="icon icon-upvote _2Jxk822qXs4DaXwsN7yyHA"></i></span></button><div class="_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ" style="color:#D7DADC">71</div><button aria-label="Downvote" aria-pressed="false" class="voteButton" data-adclicklocation="downvote" data-click-id="downvote"><span class="_1iKd82bq_nqObFvSH1iC_Q Q0BxYHtCOJ_rNSPJMU2Y7 _2fe-KdD2OM0ciaiux-G1EL _3yQIOwaIuF6gn8db96Gu7y"><i class="icon icon-downvote ZyxIIl4FP5gHGrJDzNpUC"></i></span></button></div><div class="_3-miAEojrCvx_4FQ8x3P-s"><a class="_1UoeAeSRhOKSNdY_h3iS1O _1Hw7tY9pMr-T1F4P1C-xNU _3U_7i38RDPV5eBv7m4M-9J _2qww3J5KKzsD7e5DO0BvvU" data-adclicklocation="comments" data-click-id="comments" data-testfonction-id="comments-page-link-num-comments" href="/r/cosplay/comments/14am3sh/viking_cosplay_by_akari/" rel="nofollow"><i class="icon icon-comment _3DVrpDrMM9NLT6TlsTUMxC" role="presentation"></i><span class="FHCV02u6Cp2zYL0fhQPsO"><span></span><span id="comment_t3_14am3sh_count_anim"></span>2 commentaires</span></a><div class="_3U_7i38RDPV5eBv7m4M-9J" data-adclicklocation="fl_unknown" data-ignore-click="false"><button class="_10K5i7NW6qcm-UoCtpB3aK YszYBnnIoNY8pZ6UwCivd _3yh2bniLq7bYr4BaiXowdO _1EWxiIupuIjiExPQeK4Kud _28vEaVlLWeas1CDiLuTCap"><span class="pthKOcceozMuXLYrLlbL1"><i class="_3yNNYT3e1avhAAWVHd0-92 icon icon-award" id="View--GiveAward--t3_14am3sh"></i></span><span class="_2-cXnP74241WI7fpcpfPmg _70940WUuFmpHbhKlj8EjZ">Récompenser</span></button></div><div class="_JRBNstMcGxbZUxrrIKXe _3U_7i38RDPV5eBv7m4M-9J _3yh2bniLq7bYr4BaiXowdO _1pShbCnOaF7EGWTq6IvZux _28vEaVlLWeas1CDiLuTCap" id="t3_14am3sh-share-menu"><button class="kU8ebCMnbXfjCWfqn0WPb" data-adclicklocation="fl_share" data-click-id="share"><i class="icon icon-share _1GQDWqbF-wkYWbrpmOvjqJ"></i><span class="_6_44iTtZoeY6_XChKt5b0">Partager</span></button></div><div class="_3U_7i38RDPV5eBv7m4M-9J" data-adclicklocation="fl_unknown" data-ignore-click="false"><button class="_10K5i7NW6qcm-UoCtpB3aK YszYBnnIoNY8pZ6UwCivd _3yh2bniLq7bYr4BaiXowdO _2sAFaB0tx4Hd5KxVkdUcAx _28vEaVlLWeas1CDiLuTCap"><span class="pthKOcceozMuXLYrLlbL1"><i class="_1Xe01txJfRB9udUU85DNeR icon icon-save"></i></span><span class="_2-cXnP74241WI7fpcpfPmg _70940WUuFmpHbhKlj8EjZ">Sauvegarder</span></button></div><div class="OccjSdFd6HkHhShRg6DOl"></div><div class="_3MmwvEEt6fv5kQPFCVJizH"><div><button aria-expanded="false" aria-haspopup="true" aria-label="Plus d'options" class="_2pFdCpgBihIaYh9DSMWBIu _1EbinKu2t3KjaT2gR156Qp uMPgOFYlCc5uvpa2Lbteu" data-adclicklocation="overflow_menu" id="t3_14am3sh-overflow-menu"><i class="_38GxRFSqSC-Z2VLi5Xzkjy icon icon-overflow_horizontal"></i></button></div></div><div class="_21pmAV9gWG6F_UKVe7YIE0"></div></div></div></div></div>
'''

    soup = BeautifulSoup(html, 'html.parser')

    # Récupérer l'auteur
    author = soup.find('a', {'class': '_2tbHP6ZydRpjI44J3syuqC'}).text
    print("author: ", author)
    print("=====================================")

    # Récupérer l'ID du post
    post_id = soup.find('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})['id']
    print("post_id: ", post_id)
    print("=====================================")

    # Récupérer l'image ou la vidéo
    div = soup.find('div', {'class': '_3JgI-GOrkmyIeDeyzXdyUD _2CSlKHjH7lsjx0IpjORx14'})
    if div is not None:
        #search for image
        image_url = div.find('img', {'class':'_1dwExqTGJH2jnA-MYGkEL-'})
        # search for video if image not found
        if image_url is None:
            video_url = div.find('source')['src']
            print(video_url)
    print("=====================================")
    '''
    image_url = soup.find('img', class_='_1dwExqTGJH2jnA-MYGkEL-')
    print(image_url)
    if image_url is not None:
        image_url = image_url['src']
        print("image_url: ", image_url)
    else:
        # Récupérer la vidéo
        video_url = soup.find('video', class_='_1EQJpXY7ExS04odKyfhPgw')
    '''

    # Récupérer le titre
    title = soup.find('h3', class_='_eYtD2XCVieq6emjKBH3m').text
    print("title: ", title)
    print("=====================================")



if __name__ == '__main__':
    main()
